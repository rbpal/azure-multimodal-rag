"""
Enhanced Document Processing System
Advanced PDF processing with quality assessment and structure analysis
"""

import re
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ProcessingTier(Enum):
    """Processing tiers based on document quality"""
    PREMIUM = "premium"
    STANDARD = "standard"
    BASIC = "basic"
    MANUAL_REVIEW = "manual_review"
    SKIP = "skip"


class ReviewType(Enum):
    """Types of human review needed"""
    NONE = "none"
    SPOT_CHECK = "spot_check"
    CHUNKING_VALIDATION = "chunking_validation"
    FULL_STRUCTURAL_REVIEW = "full_structural_review"
    OCR_CLEANUP = "ocr_cleanup"


@dataclass
class QualityAssessment:
    """Comprehensive document quality assessment result"""
    overall_score: float
    processing_tier: ProcessingTier
    review_type: ReviewType
    chunking_strategy: str
    estimated_processing_cost: float
    confidence_factors: Dict
    recommendations: List[str]
    should_process: bool
    priority_score: int


class EnhancedPDFReader:
    """Enhanced PDF reader with metadata and structure analysis"""
    
    def __init__(self, config=None):
        """Initialize with optional config"""
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def read_pdf_with_metadata(self, pdf_path):
        """Read PDF with comprehensive analysis"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise Exception("PyMuPDF (fitz) not installed. Run: pip install PyMuPDF")
        
        start_time = datetime.now()
        self.logger.info(f"Processing PDF: {Path(pdf_path).name}")
        
        try:
            doc = fitz.open(pdf_path)
            
            # Extract document metadata
            metadata = self._extract_document_metadata(pdf_path, doc)
            
            # Extract page content with analysis
            pages_content = self._extract_pages_content(doc)
            
            # Combine all text
            full_text = "\n".join(page['text'] for page in pages_content)
            
            # Calculate content statistics
            content_stats = self._calculate_content_statistics(full_text, pages_content)
            
            # Detect structure patterns
            structure_hints = self._detect_structure_patterns(full_text)
            
            doc.close()
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"PDF processing complete: {len(pages_content)} pages, "
                           f"{len(full_text)} chars in {processing_time:.2f}s")
            
            return {
                'content': full_text,
                'metadata': metadata,
                'pages': pages_content,
                'content_stats': content_stats,
                'structure_hints': structure_hints,
                'processing_info': {
                    'processing_time_seconds': processing_time,
                    'processed_at': datetime.now().isoformat(),
                    'processor_version': '1.0'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
    
    def _extract_document_metadata(self, pdf_path, doc):
        """Extract document and file metadata"""
        pdf_path = Path(pdf_path)
        
        # File system metadata
        file_stats = pdf_path.stat()
        
        # PDF metadata
        pdf_metadata = doc.metadata
        
        return {
            'filename': pdf_path.name,
            'file_path': str(pdf_path),
            'file_size_bytes': file_stats.st_size,
            'file_size_mb': file_stats.st_size / (1024 * 1024),
            'modified_time': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            'page_count': len(doc),
            'pdf_title': pdf_metadata.get('title', ''),
            'pdf_author': pdf_metadata.get('author', ''),
            'pdf_creator': pdf_metadata.get('creator', ''),
            'pdf_producer': pdf_metadata.get('producer', ''),
            'pdf_creation_date': pdf_metadata.get('creationDate', ''),
            'pdf_modification_date': pdf_metadata.get('modDate', '')
        }
    
    def _extract_pages_content(self, doc):
        """Extract content from each page with analysis"""
        pages = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            
            # Calculate page statistics
            char_count = len(page_text)
            word_count = len(page_text.split())
            line_count = len(page_text.splitlines())
            
            # Calculate content density
            page_rect = page.rect
            page_area = page_rect.width * page_rect.height
            char_density = char_count / page_area if page_area > 0 else 0
            
            page_info = {
                'page_number': page_num + 1,
                'text': page_text,
                'char_count': char_count,
                'word_count': word_count,
                'line_count': line_count,
                'page_width': page_rect.width,
                'page_height': page_rect.height,
                'char_density': char_density
            }
            
            pages.append(page_info)
            
            # Progress logging
            if (page_num + 1) % 10 == 0 or page_num == 0:
                self.logger.debug(f"Processed page {page_num + 1}/{len(doc)}")
        
        return pages
    
    def _calculate_content_statistics(self, full_text, pages_content):
        """Calculate comprehensive content statistics"""
        if not full_text.strip():
            return {
                'total_characters': 0,
                'total_words': 0,
                'unique_words': 0,
                'content_density': 0,
                'readability_estimate': 0
            }
        
        # Basic counts
        total_chars = len(full_text)
        words = full_text.split()
        total_words = len(words)
        unique_words = len(set(word.lower() for word in words))
        
        # Character type distribution
        alphabetic_chars = sum(1 for c in full_text if c.isalpha())
        numeric_chars = sum(1 for c in full_text if c.isdigit())
        punctuation_chars = sum(1 for c in full_text if c in '.,!?;:')
        whitespace_chars = sum(1 for c in full_text if c.isspace())
        
        # Page-level aggregations
        page_chars = [page['char_count'] for page in pages_content]
        page_words = [page['word_count'] for page in pages_content]
        page_densities = [page['char_density'] for page in pages_content]
        
        # Content density metrics
        avg_page_density = sum(page_densities) / len(page_densities) if page_densities else 0
        content_density = total_words / total_chars if total_chars > 0 else 0
        
        # Readability estimate
        readability = self._estimate_readability(full_text)
        
        return {
            'total_characters': total_chars,
            'total_words': total_words,
            'unique_words': unique_words,
            'alphabetic_chars': alphabetic_chars,
            'numeric_chars': numeric_chars,
            'punctuation_chars': punctuation_chars,
            'whitespace_chars': whitespace_chars,
            'char_type_ratios': {
                'alphabetic': alphabetic_chars / total_chars if total_chars > 0 else 0,
                'numeric': numeric_chars / total_chars if total_chars > 0 else 0,
                'punctuation': punctuation_chars / total_chars if total_chars > 0 else 0,
                'whitespace': whitespace_chars / total_chars if total_chars > 0 else 0
            },
            'page_stats': {
                'avg_chars_per_page': sum(page_chars) / len(page_chars) if page_chars else 0,
                'min_chars_per_page': min(page_chars) if page_chars else 0,
                'max_chars_per_page': max(page_chars) if page_chars else 0,
                'avg_words_per_page': sum(page_words) / len(page_words) if page_words else 0,
                'avg_page_density': avg_page_density
            },
            'content_density': content_density,
            'word_diversity_ratio': unique_words / total_words if total_words > 0 else 0,
            'readability_estimate': readability
        }
    
    def _detect_structure_patterns(self, text):
        """Detect document structure patterns"""
        if not text.strip():
            return {
                'structure_confidence': 0,
                'heading_patterns': {},
                'content_indicators': {},
                'azure_patterns': {}
            }
        
        lines = text.split('\n')
        
        # Heading pattern detection
        numbered_sections = len(re.findall(r'^\s*\d+\.\s+', text, re.MULTILINE))
        bullet_points = len(re.findall(r'^\s*[•\-\*]\s+', text, re.MULTILINE))
        all_caps_lines = len([line for line in lines if line.strip() and line.strip().isupper() and len(line.strip()) > 3])
        title_case_lines = len([line for line in lines if line.strip() and line.strip().istitle() and len(line.strip()) > 10])
        
        # Content indicators
        has_code_blocks = bool(re.search(r'```|```\w+', text)) or bool(re.search(r'^\s{4,}\w+', text, re.MULTILINE))
        has_tables = text.count('|') > 10 or bool(re.search(r'\t.*\t.*\t', text))
        url_count = len(re.findall(r'https?://[^\s]+', text))
        
        # Azure-specific patterns
        azure_services = len(re.findall(r'\bazure\s+\w+', text, re.IGNORECASE))
        azure_resource_patterns = len(re.findall(r'(vnet|subnet|nsg|vm|load.?balancer|app.?service)', text, re.IGNORECASE))
        
        # Calculate structure confidence
        structure_confidence = self._calculate_structure_confidence({
            'numbered_sections': numbered_sections,
            'bullet_points': bullet_points,
            'all_caps_lines': all_caps_lines,
            'has_code_blocks': has_code_blocks,
            'has_tables': has_tables
        })
        
        return {
            'structure_confidence': structure_confidence,
            'estimated_sections': max(numbered_sections, all_caps_lines // 2),
            'heading_patterns': {
                'numbered_sections': numbered_sections,
                'bullet_points': bullet_points,
                'all_caps_lines': all_caps_lines,
                'title_case_lines': title_case_lines
            },
            'content_indicators': {
                'has_code_blocks': has_code_blocks,
                'has_tables': has_tables,
                'has_urls': url_count,
                'url_count': url_count
            },
            'azure_patterns': {
                'azure_services': azure_services,
                'azure_resources': azure_resource_patterns,
                'total_azure_mentions': azure_services + azure_resource_patterns
            }
        }
    
    def _estimate_readability(self, text):
        """Estimate readability score (simplified Flesch Reading Ease)"""
        if not text.strip():
            return 0
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
        
        words = text.split()
        if not words:
            return 0
        
        # Simple syllable estimation (rough approximation)
        def count_syllables(word):
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllable_count += 1
                prev_was_vowel = is_vowel
            
            # Handle silent e
            if word.endswith('e') and syllable_count > 1:
                syllable_count -= 1
            
            return max(1, syllable_count)
        
        total_syllables = sum(count_syllables(word) for word in words)
        
        # Flesch Reading Ease approximation
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Normalize to 0-100 range
        return max(0, min(100, flesch_score))
    
    def _calculate_structure_confidence(self, indicators):
        """Calculate confidence in document structure"""
        confidence = 0.0
        
        # Numbered sections are strong indicators
        if indicators['numbered_sections'] > 0:
            confidence += 0.4
        
        # Bullet points indicate organization
        if indicators['bullet_points'] > 0:
            confidence += 0.2
        
        # Headers indicate structure
        if indicators['all_caps_lines'] > 0:
            confidence += 0.2
        
        # Tables and code indicate technical documentation
        if indicators['has_tables']:
            confidence += 0.1
        
        if indicators['has_code_blocks']:
            confidence += 0.1
        
        return min(1.0, confidence)


class DocumentQualityAssessor:
    """Production-ready document quality assessment system"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Quality thresholds for different processing decisions
        self.thresholds = {
            'premium_processing': 0.8,      # Top-tier processing
            'standard_processing': 0.6,     # Standard automation
            'basic_processing': 0.4,        # Minimal processing
            'manual_review': 0.2,           # Human review required
            'skip_processing': 0.1          # Don't process
        }
        
        # Cost estimates (in processing units)
        self.processing_costs = {
            ProcessingTier.PREMIUM: 10.0,
            ProcessingTier.STANDARD: 5.0,
            ProcessingTier.BASIC: 2.0,
            ProcessingTier.MANUAL_REVIEW: 15.0,  # Includes human time
            ProcessingTier.SKIP: 0.1
        }
        
        self.logger.info("Document Quality Assessor initialized")
    
    def assess_document_quality(self, pdf_data: Dict) -> QualityAssessment:
        """Comprehensive quality assessment with processing recommendations"""
        
        self.logger.info(f"Assessing quality for: {pdf_data['metadata']['filename']}")
        
        # Individual quality components
        structure_quality = self._assess_structure_quality(pdf_data)
        content_quality = self._assess_content_quality(pdf_data)
        technical_quality = self._assess_technical_quality(pdf_data)
        ocr_quality = self._assess_ocr_quality(pdf_data)
        business_value = self._assess_business_value(pdf_data)
        
        # Confidence factors for transparency
        confidence_factors = {
            'structure_quality': structure_quality,
            'content_quality': content_quality,
            'technical_quality': technical_quality,
            'ocr_quality': ocr_quality,
            'business_value': business_value
        }
        
        # Calculate weighted overall score
        overall_score = self._calculate_overall_score(confidence_factors)
        
        # Determine processing strategy
        processing_tier = self._determine_processing_tier(overall_score, confidence_factors)
        review_type = self._determine_review_type(overall_score, confidence_factors)
        chunking_strategy = self._recommend_chunking_strategy(pdf_data, overall_score)
        
        # Cost-benefit analysis
        estimated_cost = self.processing_costs[processing_tier]
        should_process = self._should_process_document(overall_score, estimated_cost, business_value)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(pdf_data, confidence_factors)
        
        # Calculate priority for processing queue
        priority_score = self._calculate_priority_score(overall_score, business_value, estimated_cost)
        
        assessment = QualityAssessment(
            overall_score=overall_score,
            processing_tier=processing_tier,
            review_type=review_type,
            chunking_strategy=chunking_strategy,
            estimated_processing_cost=estimated_cost,
            confidence_factors=confidence_factors,
            recommendations=recommendations,
            should_process=should_process,
            priority_score=priority_score
        )
        
        self.logger.info(f"Quality assessment complete: {overall_score:.2f} -> {processing_tier.value}")
        return assessment
    
    def _assess_structure_quality(self, pdf_data: Dict) -> float:
        """Assess document structure quality"""
        structure_hints = pdf_data['structure_hints']
        
        # Base score from structure confidence
        base_score = structure_hints['structure_confidence']
        
        # Bonus points for clear organization
        heading_score = 0.0
        headings = structure_hints['heading_patterns']
        
        if headings['numbered_sections'] > 0:
            heading_score += 0.3
        if headings['all_caps_lines'] > 0:
            heading_score += 0.2
        if headings['bullet_points'] > 0:
            heading_score += 0.1
        
        # Penalty for inconsistent structure
        if headings['numbered_sections'] > 0 and headings['bullet_points'] > headings['numbered_sections'] * 3:
            heading_score -= 0.1  # Too many bullets vs sections
        
        final_score = min(1.0, base_score + heading_score)
        
        self.logger.debug(f"Structure quality: {final_score:.2f} (base: {base_score:.2f}, heading: {heading_score:.2f})")
        return final_score
    
    def _assess_content_quality(self, pdf_data: Dict) -> float:
        """Assess content quality and richness"""
        content_stats = pdf_data['content_stats']
        
        # Content richness indicators
        word_diversity = content_stats['unique_words'] / max(1, content_stats['total_words'])
        content_density = content_stats['content_density']
        
        # Check for meaningful content
        if content_stats['total_words'] < 100:
            return 0.1  # Too little content
        
        # Readability assessment (context-aware)
        readability = content_stats['readability_estimate']
        
        # For technical documents, adjust readability expectations
        if self._is_technical_document(pdf_data):
            # Technical docs can have lower readability
            readability_score = max(0.5, readability / 100)
        else:
            readability_score = readability / 100
        
        # Combine factors
        quality_score = (
            word_diversity * 0.3 +
            content_density * 0.2 +
            readability_score * 0.3 +
            min(1.0, content_stats['total_words'] / 1000) * 0.2  # Length bonus up to 1000 words
        )
        
        self.logger.debug(f"Content quality: {quality_score:.2f} (diversity: {word_diversity:.2f}, density: {content_density:.2f})")
        return min(1.0, quality_score)
    
    def _assess_technical_quality(self, pdf_data: Dict) -> float:
        """Assess technical content quality for Azure documents"""
        structure_hints = pdf_data['structure_hints']
        content = pdf_data['content'].lower()
        
        # Azure-specific quality indicators
        azure_mentions = structure_hints['azure_patterns']['azure_services']
        
        # Technical terminology density
        technical_terms = [
            'configuration', 'deployment', 'management', 'security',
            'network', 'virtual', 'resource', 'service', 'endpoint',
            'policy', 'rule', 'group', 'account', 'subscription'
        ]
        
        technical_density = sum(content.count(term) for term in technical_terms) / max(1, len(content.split()))
        
        # Code and configuration indicators
        has_code = structure_hints['content_indicators']['has_code_blocks']
        has_urls = structure_hints['content_indicators']['has_urls'] > 0
        
        # Calculate technical quality
        technical_score = 0.0
        
        if azure_mentions > 10:  # Good Azure coverage
            technical_score += 0.4
        elif azure_mentions > 5:
            technical_score += 0.2
        
        if technical_density > 0.05:  # 5% technical terms
            technical_score += 0.3
        elif technical_density > 0.02:
            technical_score += 0.15
        
        if has_code:
            technical_score += 0.2
        
        if has_urls:
            technical_score += 0.1
        
        self.logger.debug(f"Technical quality: {technical_score:.2f} (Azure mentions: {azure_mentions}, tech density: {technical_density:.3f})")
        return min(1.0, technical_score)
    
    def _assess_ocr_quality(self, pdf_data: Dict) -> float:
        """Assess OCR quality and text extraction reliability"""
        content = pdf_data['content']
        
        if not content.strip():
            return 0.0
        
        # OCR quality indicators
        total_chars = len(content)
        
        # Check for OCR artifacts
        random_chars = len(re.findall(r'[^\w\s\.\,\!\?\-\(\)\:\;]', content))
        random_char_ratio = random_chars / max(1, total_chars)
        
        # Check for broken words (common OCR issue)
        words = content.split()
        short_fragments = len([w for w in words if len(w) == 1 and w.isalpha()])
        fragment_ratio = short_fragments / max(1, len(words))
        
        # Check for missing spaces (words run together)
        long_words = len([w for w in words if len(w) > 20])
        long_word_ratio = long_words / max(1, len(words))
        
        # Calculate OCR quality score
        ocr_score = 1.0
        ocr_score -= random_char_ratio * 2.0    # Penalize random characters
        ocr_score -= fragment_ratio * 1.5       # Penalize fragmentation
        ocr_score -= long_word_ratio * 1.0      # Penalize missing spaces
        
        ocr_score = max(0.0, ocr_score)
        
        self.logger.debug(f"OCR quality: {ocr_score:.2f} (random chars: {random_char_ratio:.3f}, fragments: {fragment_ratio:.3f})")
        return ocr_score
    
    def _assess_business_value(self, pdf_data: Dict) -> float:
        """Assess business value and priority of the document"""
        content = pdf_data['content'].lower()
        metadata = pdf_data['metadata']
        
        # Document freshness
        file_age_days = 0  # Could calculate from file metadata
        freshness_score = max(0.5, 1.0 - (file_age_days / 365))  # Decay over a year
        
        # Content value indicators
        value_keywords = [
            'guide', 'tutorial', 'documentation', 'best practices',
            'architecture', 'deployment', 'configuration', 'troubleshooting'
        ]
        
        value_score = sum(content.count(keyword) for keyword in value_keywords) / max(1, len(content.split()))
        value_score = min(1.0, value_score * 100)  # Scale up
        
        # Document size (comprehensive content is valuable)
        size_score = min(1.0, metadata['page_count'] / 20)  # Up to 20 pages gets full points
        
        # Combine factors
        business_value = (
            freshness_score * 0.3 +
            value_score * 0.4 +
            size_score * 0.3
        )
        
        self.logger.debug(f"Business value: {business_value:.2f} (freshness: {freshness_score:.2f}, value: {value_score:.2f})")
        return business_value
    
    def _calculate_overall_score(self, confidence_factors: Dict) -> float:
        """Calculate weighted overall quality score"""
        weights = {
            'structure_quality': 0.25,
            'content_quality': 0.25,
            'technical_quality': 0.20,
            'ocr_quality': 0.20,
            'business_value': 0.10
        }
        
        overall_score = sum(
            confidence_factors[factor] * weight 
            for factor, weight in weights.items()
        )
        
        return min(1.0, overall_score)
    
    def _determine_processing_tier(self, overall_score: float, confidence_factors: Dict) -> ProcessingTier:
        """Determine appropriate processing tier"""
        # Check for specific issues that override score
        if confidence_factors['ocr_quality'] < 0.3:
            return ProcessingTier.MANUAL_REVIEW
        
        # Score-based tiers
        if overall_score >= self.thresholds['premium_processing']:
            return ProcessingTier.PREMIUM
        elif overall_score >= self.thresholds['standard_processing']:
            return ProcessingTier.STANDARD
        elif overall_score >= self.thresholds['basic_processing']:
            return ProcessingTier.BASIC
        elif overall_score >= self.thresholds['manual_review']:
            return ProcessingTier.MANUAL_REVIEW
        else:
            return ProcessingTier.SKIP
    
    def _determine_review_type(self, overall_score: float, confidence_factors: Dict) -> ReviewType:
        """Determine type of human review needed"""
        if confidence_factors['ocr_quality'] < 0.5:
            return ReviewType.OCR_CLEANUP
        elif confidence_factors['structure_quality'] < 0.3:
            return ReviewType.FULL_STRUCTURAL_REVIEW
        elif overall_score < 0.6:
            return ReviewType.CHUNKING_VALIDATION
        elif overall_score >= 0.8:
            return ReviewType.NONE
        else:
            return ReviewType.SPOT_CHECK
    
    def _recommend_chunking_strategy(self, pdf_data: Dict, overall_score: float) -> str:
        """Recommend chunking strategy based on quality assessment"""
        structure_confidence = pdf_data['structure_hints']['structure_confidence']
        
        if overall_score >= 0.8 and structure_confidence >= 0.7:
            return "semantic_section_based"
        elif overall_score >= 0.6 and structure_confidence >= 0.5:
            return "smart_boundary_chunking"
        elif overall_score >= 0.4:
            return "sentence_boundary_chunking"
        else:
            return "fixed_size_chunking"
    
    def _should_process_document(self, overall_score: float, estimated_cost: float, business_value: float) -> bool:
        """Cost-benefit analysis for processing decision"""
        # Simple ROI calculation
        expected_benefit = overall_score * business_value * 10  # Scale factor
        roi = expected_benefit / max(0.1, estimated_cost)
        
        # Process if ROI > 1.0 and minimum quality threshold met
        return roi > 1.0 and overall_score > 0.2
    
    def _generate_recommendations(self, pdf_data: Dict, confidence_factors: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if confidence_factors['structure_quality'] < 0.5:
            recommendations.append("Consider manual section marking for better structure detection")
        
        if confidence_factors['ocr_quality'] < 0.7:
            recommendations.append("OCR quality issues detected - consider reprocessing with better OCR")
        
        if confidence_factors['technical_quality'] < 0.3:
            recommendations.append("Low technical content density - verify document relevance")
        
        if pdf_data['content_stats']['total_words'] < 500:
            recommendations.append("Short document - consider combining with related documents")
        
        azure_services = pdf_data['structure_hints']['azure_patterns']['azure_services']
        if azure_services > 50:
            recommendations.append("High Azure service density - consider specialized Azure chunking")
        
        return recommendations
    
    def _calculate_priority_score(self, overall_score: float, business_value: float, estimated_cost: float) -> int:
        """Calculate priority score for processing queue (0-100)"""
        # Higher score = higher priority
        priority = (overall_score * 40 + business_value * 40 + (10 / max(1, estimated_cost)) * 20)
        return min(100, int(priority * 100))
    
    def _is_technical_document(self, pdf_data: Dict) -> bool:
        """Detect if document is technical in nature"""
        azure_mentions = pdf_data['structure_hints']['azure_patterns']['azure_services']
        technical_indicators = pdf_data['structure_hints']['content_indicators']
        
        return (
            azure_mentions > 5 or
            technical_indicators['has_code_blocks'] or
            technical_indicators['has_urls'] > 2
        )