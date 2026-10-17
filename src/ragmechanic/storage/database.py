import sqlite3
from pathlib import Path
from datetime import datetime

from langchain_core.documents import Document

from ..report.result import RAGResult
from ..evaluation.result import EvaluationResult


class Database:

    def __init__(self, db_path="ragmechanic.db"):
        self.db_path = Path(db_path)
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):

        with self._connect() as conn:

            cursor = conn.cursor()

            # =================================================
            # QUERIES
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,

                    retrieval_latency REAL,
                    compression_latency REAL,
                    generation_latency REAL,
                    total_latency REAL,

                    retrieved_count INTEGER,
                    compressed_count INTEGER,
                    compression_ratio REAL,

                    created_at TEXT
                )
            """)

            # =================================================
            # RETRIEVED CHUNKS
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS retrieved_chunks (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    query_id INTEGER,

                    content TEXT,

                    source TEXT,
                    page TEXT,
                    chunk_id INTEGER,
                    rank INTEGER,
                    similarity_score REAL,

                    FOREIGN KEY(query_id)
                        REFERENCES queries(id)
                )
            """)

            # =================================================
            # COMPRESSED CHUNKS
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compressed_chunks (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    query_id INTEGER,

                    content TEXT,

                    source TEXT,
                    page TEXT,
                    chunk_id INTEGER,
                    rank INTEGER,
                    similarity_score REAL,

                    FOREIGN KEY(query_id)
                        REFERENCES queries(id)
                )
            """)

            # =================================================
            # EVALUATIONS
            # =================================================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    query_id INTEGER UNIQUE,

                    faithfulness REAL,
                    answer_relevancy REAL,
                    hallucination REAL,

                    evaluated_at TEXT,

                    FOREIGN KEY(query_id)
                        REFERENCES queries(id)
                )
            """)

            conn.commit()

    # =========================================================
    # SAVE RAG RESULT
    # =========================================================

    def save_result(self, result: RAGResult):

        with self._connect() as conn:

            cursor = conn.cursor()

            # -------------------------------------------------
            # Save query
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO queries (

                    question,
                    answer,

                    retrieval_latency,
                    compression_latency,
                    generation_latency,
                    total_latency,

                    retrieved_count,
                    compressed_count,
                    compression_ratio,

                    created_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.question,
                    result.answer,

                    result.retrieval_latency,
                    result.compression_latency,
                    result.generation_latency,
                    result.total_latency,

                    result.retrieved_count,
                    result.compressed_count,
                    result.compression_ratio,

                    datetime.now().isoformat(),
                )
            )

            query_id = cursor.lastrowid

            # -------------------------------------------------
            # Save retrieved chunks
            # -------------------------------------------------

            for doc in result.retrieved_documents:

                self._insert_chunk(
                    cursor,
                    table="retrieved_chunks",
                    query_id=query_id,
                    doc=doc
                )

            # -------------------------------------------------
            # Save compressed chunks
            # -------------------------------------------------

            for doc in result.compressed_documents:

                self._insert_chunk(
                    cursor,
                    table="compressed_chunks",
                    query_id=query_id,
                    doc=doc
                )

            conn.commit()

        return query_id

    # =========================================================
    # INSERT CHUNK
    # =========================================================

    def _insert_chunk(
        self,
        cursor,
        table,
        query_id,
        doc
    ):

        metadata = doc.metadata

        cursor.execute(
            f"""
            INSERT INTO {table} (

                query_id,
                content,

                source,
                page,
                chunk_id,
                rank,
                similarity_score

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                query_id,

                doc.page_content,

                metadata.get("source"),

                str(
                    metadata.get(
                        "page",
                        ""
                    )
                ),

                metadata.get("chunk_id"),

                metadata.get("rank"),

                metadata.get(
                    "similarity_score"
                ),
            )
        )

    # =========================================================
    # GET UNEVALUATED QUERY IDS
    # =========================================================

    def get_unevaluated_query_ids(self):

        with self._connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT q.id

                FROM queries q

                LEFT JOIN evaluations e
                    ON q.id = e.query_id

                WHERE e.query_id IS NULL

                ORDER BY q.id
            """)

            return [
                row[0]
                for row in cursor.fetchall()
            ]

    # =========================================================
    # GET QUERY
    # =========================================================

    def get_query(self, query_id):

        with self._connect() as conn:

            cursor = conn.cursor()

            # -------------------------------------------------
            # Query
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT

                    id,
                    question,
                    answer,

                    retrieval_latency,
                    compression_latency,
                    generation_latency,

                    retrieved_count,
                    compressed_count,
                    compression_ratio

                FROM queries

                WHERE id = ?
                """,
                (query_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            (
                id_,
                question,
                answer,

                retrieval_latency,
                compression_latency,
                generation_latency,

                retrieved_count,
                compressed_count,
                compression_ratio,

            ) = row

            # -------------------------------------------------
            # Retrieved documents
            # -------------------------------------------------

            retrieved_documents = self._get_chunks(
                cursor,
                table="retrieved_chunks",
                query_id=query_id
            )

            # -------------------------------------------------
            # Compressed documents
            # -------------------------------------------------

            compressed_documents = self._get_chunks(
                cursor,
                table="compressed_chunks",
                query_id=query_id
            )

            # -------------------------------------------------
            # Evaluation
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT

                    faithfulness,
                    answer_relevancy,
                    hallucination

                FROM evaluations

                WHERE query_id = ?
                """,
                (query_id,)
            )

            evaluation_row = cursor.fetchone()

            evaluation = None

            if evaluation_row:

                (
                    faithfulness,
                    answer_relevancy,
                    hallucination,
                ) = evaluation_row

                evaluation = EvaluationResult(
                    faithfulness=faithfulness,
                    answer_relevancy=answer_relevancy,
                    hallucination=hallucination,
                )

        return RAGResult(

            id=id_,

            question=question,

            answer=answer,

            retrieved_documents=retrieved_documents,

            compressed_documents=compressed_documents,

            retrieval_latency=
                retrieval_latency or 0.0,

            compression_latency=
                compression_latency or 0.0,

            generation_latency=
                generation_latency or 0.0,

            evaluation=evaluation,
        )

    # =========================================================
    # GET CHUNKS
    # =========================================================

    def _get_chunks(
        self,
        cursor,
        table,
        query_id
    ):

        cursor.execute(
            f"""
            SELECT

                content,
                source,
                page,
                chunk_id,
                rank,
                similarity_score

            FROM {table}

            WHERE query_id = ?

            ORDER BY
                rank
            """,
            (query_id,)
        )

        rows = cursor.fetchall()

        documents = []

        for row in rows:

            (
                content,
                source,
                page,
                chunk_id,
                rank,
                similarity_score,
            ) = row

            metadata = {

                "source": source,

                "page": page,

                "chunk_id": chunk_id,

                "rank": rank,

                "similarity_score":
                    similarity_score,
            }

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

        return documents

    # =========================================================
    # SAVE EVALUATION
    # =========================================================

    def save_evaluation(
        self,
        query_id,
        evaluation: EvaluationResult
    ):

        with self._connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO evaluations (

                    query_id,

                    faithfulness,

                    answer_relevancy,

                    hallucination,

                    evaluated_at

                )

                VALUES (?, ?, ?, ?, ?)

                ON CONFLICT(query_id)

                DO UPDATE SET

                    faithfulness =
                        excluded.faithfulness,

                    answer_relevancy =
                        excluded.answer_relevancy,

                    hallucination =
                        excluded.hallucination,

                    evaluated_at =
                        excluded.evaluated_at
                """,
                (
                    query_id,

                    getattr(
                        evaluation,
                        "faithfulness",
                        None
                    ),

                    getattr(
                        evaluation,
                        "answer_relevancy",
                        None
                    ),

                    getattr(
                        evaluation,
                        "hallucination",
                        None
                    ),

                    datetime.now().isoformat(),
                )
            )

            conn.commit()

    # =========================================================
    # GET ALL QUERIES
    # =========================================================

    def get_all_queries(self):

        with self._connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id

                FROM queries

                ORDER BY id
            """)

            ids = [
                row[0]
                for row in cursor.fetchall()
            ]

        return [
            self.get_query(query_id)
            for query_id in ids
        ]
