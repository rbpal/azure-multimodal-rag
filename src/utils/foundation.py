"""
Azure RAG Foundation Components
Core classes for PDF reading, text chunking, and basic search
"""

import re
import json
import pickle
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import List, Dict, Optional, Tuple, Union


class SimplePDFReader:
    """Simple PDF reader using PyMuPDF"""
    
    def __init__(self, config=None):
        """Initialize with optional config"""
        self.config = config
        
    def read_pdf(self, pdf_path):
        """Read a PDF file and return text content"""
        try:
            import fitz  # PyMuPDF
            
            # Open the PDF
            doc = fitz.open(pdf_path)
            text_content = ""
            
            print(f"📄 Processing {len(doc)} pages...")
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                text_content += page_text
                
                # Show progress for larger documents
                if (page_num + 1) % 5 == 0 or page_num == 0:
                    print(f"   📖 Processed page {page_num + 1}/{len(doc)}")
            
            doc.close()
            return text_content
            
        except ImportError:
            raise Exception("PyMuPDF (fitz) not installed. Run: pip install PyMuPDF")
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")


class SmartTextChunker:
    """Intelligent text chunking for Azure RAG system"""
    
    def __init__(self, config):
        """Initialize with configuration settings"""
        self.config = config
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        
        print(f"🎯 Chunker initialized:")
        print(f"   📏 Chunk size: {self.chunk_size} characters")
        print(f"   🔄 Overlap: {self.chunk_overlap} characters ({self.chunk_overlap/self.chunk_size*100:.1f}%)")
    
    def clean_text(self, text):
        """Clean and normalize text before chunking"""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive line breaks (keep paragraph breaks)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def find_sentence_boundary(self, text, ideal_position):
        """Find the best place to split text (prefer sentence endings)"""
        # Don't search past the end of text
        if ideal_position >= len(text):
            return len(text)
            
        # Look for sentence endings near the ideal position
        search_range = min(100, len(text) - ideal_position)
        
        # Search backwards from ideal position for sentence endings
        for i in range(ideal_position, max(0, ideal_position - search_range), -1):
            if i < len(text) and text[i] in '.!?':
                # Make sure it's not just an abbreviation
                if i + 1 < len(text) and text[i + 1] in ' \n':
                    return i + 1
        
        # If no sentence ending found, look for paragraph breaks
        for i in range(ideal_position, max(0, ideal_position - search_range), -1):
            if i < len(text) and text[i] == '\n':
                return i + 1
        
        # If nothing found, use the ideal position
        return ideal_position
    
    def create_chunks(self, text, source_info="Unknown"):
        """Split text into overlapping chunks with smart boundaries"""
        
        # Clean the text first
        text = self.clean_text(text)
        
        print(f"📝 Processing text: {len(text):,} characters")
        
        if len(text) <= self.chunk_size:
            # Text is small enough to be one chunk
            return [{
                'content': text,
                'chunk_id': 0,
                'source': source_info,
                'char_start': 0,
                'char_end': len(text),
                'char_count': len(text),
                'word_count': len(text.split())
            }]
        
        chunks = []
        start_pos = 0
        chunk_id = 0
        
        print(f"📦 Starting chunking process...")
        
        while start_pos < len(text):
            # Calculate ideal end position
            ideal_end = start_pos + self.chunk_size
            
            if ideal_end >= len(text):
                # Last chunk - take remaining text
                end_pos = len(text)
            else:
                # Find smart boundary
                end_pos = self.find_sentence_boundary(text, ideal_end)
            
            # Extract chunk content
            chunk_content = text[start_pos:end_pos].strip()
            
            if chunk_content:  # Only add non-empty chunks
                chunk = {
                    'content': chunk_content,
                    'chunk_id': chunk_id,
                    'source': source_info,
                    'char_start': start_pos,
                    'char_end': end_pos,
                    'char_count': len(chunk_content),
                    'word_count': len(chunk_content.split())
                }
                chunks.append(chunk)
                chunk_id += 1
                
                # Show progress for first few chunks
                if chunk_id <= 3:
                    print(f"   📦 Chunk {chunk_id}: {start_pos}-{end_pos} ({len(chunk_content)} chars)")
            
            # Calculate next starting position with proper overlap
            next_start = end_pos - self.chunk_overlap
            
            # Ensure meaningful progress to prevent tiny chunks
            min_progress = max(self.chunk_size - self.chunk_overlap - 50, 200)
            
            if next_start <= start_pos:
                # If overlap is too big, make reasonable progress
                next_start = start_pos + min_progress
            elif (next_start - start_pos) < min_progress:
                # If we're not making enough progress, force a bigger step
                next_start = start_pos + min_progress
            
            # Safety: if we're near the end, just finish
            if next_start >= len(text) - 50:
                break
                
            start_pos = next_start
            
            # Safety check to prevent infinite loops
            if chunk_id > 100:  # Reasonable limit for any document
                print(f"⚠️  Safety limit reached at {chunk_id} chunks")
                break
        
        print(f"✅ Chunking complete: {len(chunks)} chunks created")
        return chunks
    
    def analyze_chunks(self, chunks):
        """Analyze chunk statistics"""
        if not chunks:
            return {}
        
        char_counts = [chunk['char_count'] for chunk in chunks]
        word_counts = [chunk['word_count'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chars': sum(char_counts) / len(char_counts),
            'min_chars': min(char_counts),
            'max_chars': max(char_counts),
            'avg_words': sum(word_counts) / len(word_counts),
            'total_chars': sum(char_counts),
            'total_words': sum(word_counts)
        }


class BasicTextSearcher:
    """Simple but effective text search for Azure RAG foundation"""
    
    def __init__(self, config):
        """Initialize with configuration"""
        self.config = config
        self.chunks = []  # Will store our text chunks
        self.search_index = {}  # Simple keyword index
        
        print(f"🎯 Search system initialized")
        print(f"   🔍 Ready to index chunks")
        print(f"   📊 Will track search statistics")
    
    def add_chunks(self, chunks: List[Dict]):
        """Add chunks to our search system"""
        self.chunks.extend(chunks)
        self._build_search_index(chunks)
        
        print(f"📚 Added {len(chunks)} chunks to search index")
        print(f"   📦 Total chunks in system: {len(self.chunks)}")
        print(f"   🔑 Index contains {len(self.search_index)} unique terms")
    
    def _build_search_index(self, chunks: List[Dict]):
        """Build a simple keyword index for fast searching"""
        for chunk in chunks:
            chunk_id = chunk['chunk_id']
            text = chunk['content'].lower()
            
            # Extract words (simple tokenization)
            words = re.findall(r'\b\w+\b', text)
            
            # Add to inverted index
            for word in words:
                if word not in self.search_index:
                    self.search_index[word] = []
                
                # Only add if not already there (avoid duplicates)
                if chunk_id not in [item['chunk_id'] for item in self.search_index[word]]:
                    self.search_index[word].append({
                        'chunk_id': chunk_id,
                        'source': chunk['source']
                    })
    
    def _calculate_relevance_score(self, chunk: Dict, query_terms: List[str]) -> float:
        """Calculate how relevant a chunk is to the query"""
        content = chunk['content'].lower()
        score = 0.0
        
        # Count term matches
        for term in query_terms:
            term_count = content.count(term.lower())
            if term_count > 0:
                # Term frequency score (more mentions = higher score)
                tf_score = term_count / len(content.split())
                score += tf_score
                
                # Bonus for exact phrase matches
                if len(query_terms) > 1 and ' '.join(query_terms).lower() in content:
                    score += 0.5
        
        # Bonus for Azure-specific terms (domain relevance)
        azure_terms = ['azure', 'vnet', 'subnet', 'nsg', 'load balancer', 'network']
        azure_bonus = sum(1 for term in azure_terms if term in content) * 0.1
        score += azure_bonus
        
        return score
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for chunks matching the query"""
        if not query.strip():
            return []
        
        print(f"\n🔍 Searching for: '{query}'")
        
        # Prepare query terms
        query_terms = re.findall(r'\b\w+\b', query.lower())
        print(f"   📝 Query terms: {query_terms}")
        
        # Find candidate chunks
        candidate_chunks = set()
        
        for term in query_terms:
            if term in self.search_index:
                for item in self.search_index[term]:
                    candidate_chunks.add(item['chunk_id'])
        
        print(f"   📦 Found {len(candidate_chunks)} candidate chunks")
        
        if not candidate_chunks:
            print(f"   ❌ No matches found")
            return []
        
        # Score and rank chunks
        scored_chunks = []
        
        for chunk_id in candidate_chunks:
            # Find the actual chunk
            chunk = next((c for c in self.chunks if c['chunk_id'] == chunk_id), None)
            if chunk:
                score = self._calculate_relevance_score(chunk, query_terms)
                if score > 0:
                    scored_chunks.append({
                        'chunk': chunk,
                        'score': score,
                        'matched_terms': [term for term in query_terms 
                                        if term in chunk['content'].lower()]
                    })
        
        # Sort by relevance score (highest first)
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top results
        results = scored_chunks[:max_results]
        
        print(f"   ✅ Returning top {len(results)} results")
        for i, result in enumerate(results, 1):
            print(f"      {i}. Score: {result['score']:.3f} | Terms: {result['matched_terms']}")
        
        return results
    
    def get_search_statistics(self) -> Dict:
        """Get statistics about the search system"""
        if not self.chunks:
            return {'status': 'empty'}
        
        # Calculate statistics
        chunk_sizes = [len(chunk['content']) for chunk in self.chunks]
        sources = [chunk['source'] for chunk in self.chunks]
        source_counts = Counter(sources)
        
        return {
            'total_chunks': len(self.chunks),
            'total_terms_indexed': len(self.search_index),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'sources': dict(source_counts),
            'memory_estimate_mb': (sum(chunk_sizes) * 4) / (1024 * 1024)  # Rough estimate
        }


class SimpleStorageManager:
    """Simple but robust storage for Azure RAG foundation"""
    
    def __init__(self, config):
        """Initialize with configuration"""
        self.config = config
        self.storage_path = Path(config.PROCESSED_FOLDER)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Storage system initialized")
        print(f"   📁 Storage location: {self.storage_path}")
        print(f"   🔧 Ready to save/load chunks and search indices")
    
    def _generate_session_id(self):
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"
    
    def _calculate_content_hash(self, content):
        """Calculate hash of content for change detection"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
    
    def save_chunks(self, chunks, source_name="unknown", session_id=None):
        """Save chunks to storage with metadata"""
        if not chunks:
            print("⚠️  No chunks to save")
            return None
        
        # Generate session ID if not provided
        if session_id is None:
            session_id = self._generate_session_id()
        
        # Prepare storage data
        storage_data = {
            'metadata': {
                'session_id': session_id,
                'source_name': source_name,
                'created_at': datetime.now().isoformat(),
                'total_chunks': len(chunks),
                'chunk_size_config': self.config.CHUNK_SIZE,
                'chunk_overlap_config': self.config.CHUNK_OVERLAP,
                'total_characters': sum(chunk['char_count'] for chunk in chunks),
                'total_words': sum(chunk['word_count'] for chunk in chunks)
            },
            'chunks': chunks
        }
        
        # Save as JSON (human readable)
        json_file = self.storage_path / f"{session_id}_chunks.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)
        
        # Save as pickle (faster loading)
        pickle_file = self.storage_path / f"{session_id}_chunks.pkl"
        with open(pickle_file, 'wb') as f:
            pickle.dump(storage_data, f)
        
        print(f"✅ Saved {len(chunks)} chunks:")
        print(f"   📄 JSON: {json_file.name}")
        print(f"   🚀 Pickle: {pickle_file.name}")
        print(f"   🔖 Session ID: {session_id}")
        
        return session_id
    
    def load_chunks(self, session_id):
        """Load chunks from storage"""
        pickle_file = self.storage_path / f"{session_id}_chunks.pkl"
        json_file = self.storage_path / f"{session_id}_chunks.json"
        
        # Try pickle first (faster)
        if pickle_file.exists():
            print(f"📚 Loading from pickle: {pickle_file.name}")
            with open(pickle_file, 'rb') as f:
                data = pickle.load(f)
        elif json_file.exists():
            print(f"📚 Loading from JSON: {json_file.name}")
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            print(f"❌ Session not found: {session_id}")
            return None, None
        
        chunks = data['chunks']
        metadata = data['metadata']
        
        print(f"✅ Loaded {len(chunks)} chunks from {metadata['source_name']}")
        print(f"   📅 Created: {metadata['created_at']}")
        print(f"   📊 Total chars: {metadata['total_characters']:,}")
        print(f"   📄 Total words: {metadata['total_words']:,}")
        
        return chunks, metadata
    
    def save_search_index(self, searcher, session_id):
        """Save search index and statistics"""
        if not hasattr(searcher, 'search_index'):
            print("⚠️  No search index to save")
            return
        
        # Prepare index data
        index_data = {
            'metadata': {
                'session_id': session_id,
                'created_at': datetime.now().isoformat(),
                'total_chunks_indexed': len(searcher.chunks),
                'total_terms': len(searcher.search_index),
                'statistics': searcher.get_search_statistics()
            },
            'search_index': searcher.search_index,
            'chunks_metadata': [{
                'chunk_id': chunk['chunk_id'],
                'source': chunk['source'],
                'char_count': chunk['char_count']
            } for chunk in searcher.chunks]
        }
        
        # Save index
        index_file = self.storage_path / f"{session_id}_search_index.pkl"
        with open(index_file, 'wb') as f:
            pickle.dump(index_data, f)
        
        print(f"✅ Saved search index:")
        print(f"   🔍 File: {index_file.name}")
        print(f"   📊 Terms indexed: {len(searcher.search_index):,}")
        print(f"   📦 Chunks indexed: {len(searcher.chunks)}")
    
    def load_search_index(self, session_id):
        """Load search index"""
        index_file = self.storage_path / f"{session_id}_search_index.pkl"
        
        if not index_file.exists():
            print(f"❌ Search index not found: {session_id}")
            return None
        
        with open(index_file, 'rb') as f:
            index_data = pickle.load(f)
        
        metadata = index_data['metadata']
        search_index = index_data['search_index']
        
        print(f"✅ Loaded search index:")
        print(f"   📅 Created: {metadata['created_at']}")
        print(f"   🔍 Terms: {len(search_index):,}")
        print(f"   📦 Chunks: {metadata['total_chunks_indexed']}")
        
        return search_index, metadata
    
    def list_saved_sessions(self):
        """List all saved sessions"""
        json_files = list(self.storage_path.glob("*_chunks.json"))
        
        if not json_files:
            print("📭 No saved sessions found")
            return []
        
        sessions = []
        print(f"📚 Found {len(json_files)} saved sessions:")
        
        for json_file in sorted(json_files):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data['metadata']
                session_id = metadata['session_id']
                
                # Check for corresponding files
                has_pickle = (self.storage_path / f"{session_id}_chunks.pkl").exists()
                has_index = (self.storage_path / f"{session_id}_search_index.pkl").exists()
                
                session_info = {
                    'session_id': session_id,
                    'source_name': metadata['source_name'],
                    'created_at': metadata['created_at'],
                    'total_chunks': metadata['total_chunks'],
                    'has_pickle': has_pickle,
                    'has_search_index': has_index
                }
                
                sessions.append(session_info)
                
                print(f"   📄 {session_id}")
                print(f"      📚 Source: {metadata['source_name']}")
                print(f"      📅 Created: {metadata['created_at']}")
                print(f"      📦 Chunks: {metadata['total_chunks']}")
                print(f"      🚀 Pickle: {'✅' if has_pickle else '❌'}")
                print(f"      🔍 Index: {'✅' if has_index else '❌'}")
                
            except Exception as e:
                print(f"   ⚠️  Error reading {json_file.name}: {e}")
        
        return sessions
    
    def cleanup_old_sessions(self, keep_latest=5):
        """Keep only the latest N sessions"""
        sessions = self.list_saved_sessions()
        
        if len(sessions) <= keep_latest:
            print(f"📚 Only {len(sessions)} sessions found, keeping all")
            return
        
        # Sort by creation time and keep latest
        sessions.sort(key=lambda x: x['created_at'], reverse=True)
        sessions_to_delete = sessions[keep_latest:]
        
        print(f"🧹 Cleaning up {len(sessions_to_delete)} old sessions...")
        
        for session in sessions_to_delete:
            session_id = session['session_id']
            
            # Delete all files for this session
            files_to_delete = [
                f"{session_id}_chunks.json",
                f"{session_id}_chunks.pkl", 
                f"{session_id}_search_index.pkl"
            ]
            
            for filename in files_to_delete:
                file_path = self.storage_path / filename
                if file_path.exists():
                    file_path.unlink()
                    print(f"   🗑️  Deleted: {filename}")
        
        print(f"✅ Cleanup complete, kept {keep_latest} latest sessions")