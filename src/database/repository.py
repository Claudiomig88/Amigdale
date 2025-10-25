import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseRepository:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL environment variable not set. "
                "Please ensure PostgreSQL database is configured."
            )
        try:
            self.init_database()
        except Exception as e:
            raise ValueError(
                f"Failed to initialize database: {e}. "
                "Please check DATABASE_URL and PostgreSQL connection."
            ) from e
    
    def get_connection(self):
        return psycopg2.connect(self.database_url)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id SERIAL PRIMARY KEY,
                topic_name VARCHAR(500) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id SERIAL PRIMARY KEY,
                topic_id INTEGER REFERENCES topics(id),
                topic_name VARCHAR(500) NOT NULL,
                script TEXT,
                youtube_id VARCHAR(100),
                youtube_url VARCHAR(500),
                status VARCHAR(50) DEFAULT 'pending',
                cost_images DECIMAL(10, 2) DEFAULT 0,
                cost_audio DECIMAL(10, 2) DEFAULT 0,
                cost_music DECIMAL(10, 2) DEFAULT 0,
                cost_script DECIMAL(10, 2) DEFAULT 0,
                total_cost DECIMAL(10, 2) DEFAULT 0,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_logs (
                id SERIAL PRIMARY KEY,
                video_id INTEGER REFERENCES videos(id),
                agent_name VARCHAR(100),
                status VARCHAR(50),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def add_topic(self, topic_name: str) -> Optional[int]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO topics (topic_name) VALUES (%s) RETURNING id',
                (topic_name,)
            )
            result = cursor.fetchone()
            if result:
                topic_id = result[0]
                conn.commit()
                return topic_id
            return None
        except psycopg2.IntegrityError:
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()
    
    def is_topic_used(self, topic_name: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT used FROM topics WHERE topic_name = %s',
            (topic_name,)
        )
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result and len(result) > 0:
            return result[0]
        return False
    
    def mark_topic_used(self, topic_name: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE topics SET used = TRUE WHERE topic_name = %s',
            (topic_name,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def create_video(self, topic_name: str) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO videos (topic_name) VALUES (%s) RETURNING id',
            (topic_name,)
        )
        result = cursor.fetchone()
        if result:
            video_id = result[0]
        else:
            raise ValueError("Failed to create video record")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return video_id
    
    def update_video(self, video_id: int, **kwargs):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clauses = []
        values = []
        
        for key, value in kwargs.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        
        values.append(video_id)
        
        query = f"UPDATE videos SET {', '.join(set_clauses)} WHERE id = %s"
        cursor.execute(query, values)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def add_log(self, video_id: int, agent_name: str, status: str, message: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO production_logs (video_id, agent_name, status, message) 
               VALUES (%s, %s, %s, %s)''',
            (video_id, agent_name, status, message)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_all_videos(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            '''SELECT * FROM videos 
               ORDER BY created_at DESC 
               LIMIT 100'''
        )
        videos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [dict(v) for v in videos]
    
    def get_video_logs(self, video_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            '''SELECT * FROM production_logs 
               WHERE video_id = %s 
               ORDER BY created_at ASC''',
            (video_id,)
        )
        logs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [dict(log) for log in logs]
    
    def get_statistics(self) -> Dict:
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_videos,
                COUNT(CASE WHEN status = 'published' THEN 1 END) as published,
                COUNT(CASE WHEN status = 'error' THEN 1 END) as errors,
                AVG(total_cost) as avg_cost,
                SUM(total_cost) as total_cost
            FROM videos
        ''')
        
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return dict(stats) if stats else {}
