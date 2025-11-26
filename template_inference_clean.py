#!/usr/bin/env python3
"""
Template Inference Engine with Page Number-Based Approach
Enhanced version that uses page numbers instead of page types for better mixed content handling
"""

import json
from typing import List, Dict, Any, Optional
from collections import defaultdict, Counter
import re
from bedrock_client import BedrockClient
from catalog_integration import CatalogIntegration

class TemplateInferenceEngine:
    def __init__(self, bedrock_client: BedrockClient):
        self.bedrock_client = bedrock_client
        self.catalog = CatalogIntegration()

    def infer_master_template(self, per_page_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive master template using page number approach"""
        
        # Step 1: Map all detected elements to catalog
        all_detected_elements = []
        for page_doc in per_page_docs:
            all_detected_elements.extend(page_doc.get('elements', []))
        
        mapped_elements = self.catalog.map_detected_elements(all_detected_elements)
        
        # Step 2: Analyze catalog coverage
        coverage_analysis = self.catalog.analyze_catalog_coverage(all_detected_elements)
        
        # Step 3: Analyze document structure
        doc_analysis = self._analyze_document_structure(per_page_docs)
        
        # Step 4: Group pages by page number instead of semantic type
        page_groups = self._group_pages_by_number(per_page_docs)
        
        # Step 5: Identify common elements using catalog mapping
        common_elements = self._identify_common_elements_with_catalog(per_page_docs, mapped_elements)
        
        # Step 6: Analyze element frequency with catalog integration
        element_frequency = self._analyze_element_frequency_with_catalog(per_page_docs, mapped_elements)
        
        # Step 7: Create template pages with page number approach
        template_pages = []
        document_fields = {}
        document_metadata = {}
        
        # Get maximum page count across all documents
        max_pages = max([max([doc.get('page_index', 1) for doc in per_page_docs if doc.get('doc_id') == doc_id] + [1]) 
                        for doc_id in set(doc.get('doc_id') for doc in per_page_docs)])
        
        for page_num in range(1, max_pages + 1):
            if page_num in page_groups:
                pages_for_number = page_groups[page_num]
                template_page = self._create_page_number_template(
                    page_num, pages_for_number, document_fields, document_metadata, element_frequency, mapped_elements
                )
                if template_page:
                    template_pages.append(template_page)
        
        # Step 8: Build final template structure with page numbers
        sorted_pages = sorted(template_pages, key=lambda x: x['page_number'])
        
        master_template = {
            "template_id": "page_number_based_master_v1",
            "name": "Page Number-Based Master Template",
            "description": f"Master template built from {len(set(doc['doc_id'] for doc in per_page_docs))} documents using page number approach",
            "doc_type": "comprehensive_document",
            "output_format": "pptx",
            "catalog_integration": {
                "catalog_id": self.catalog.master_catalog.get('template_id', 'unknown'),
                "catalog_version": self.catalog.master_catalog.get('version', '1.0'),
                "catalog_name": self.catalog.master_catalog.get('name', 'Unknown'),
                "coverage_analysis": coverage_analysis,
                "mapped_elements": len([e for e in mapped_elements if e['mapping_status'] == 'mapped']),
                "unmapped_elements": len([e for e in mapped_elements if e['mapping_status'] == 'unmapped'])
            },
            "analysis_summary": {
                "total_documents": len(set(doc['doc_id'] for doc in per_page_docs)),
                "total_pages": len(per_page_docs),
                "common_elements": len(common_elements),
                "unique_elements": len(element_frequency),
                "document_structure": doc_analysis
            },
            "document_metadata": document_metadata,
            "document_fields": list(document_fields.values()),
            "common_elements": common_elements,
            "element_frequency": element_frequency,
            "pages": sorted_pages,
            "total_pages": len(sorted_pages),
            "max_page_number": max_pages if sorted_pages else 0
        }
        
        return master_template

    def _group_pages_by_number(self, per_page_docs: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """Group pages by page number across documents"""
        page_groups = defaultdict(list)
        
        for page_doc in per_page_docs:
            page_num = page_doc.get('page_index', 1)
            page_groups[page_num].append(page_doc)
        
        return dict(page_groups)

    def _create_page_number_template(self, page_num: int, pages: List[Dict[str, Any]], 
                                   document_fields: Dict[str, Any], document_metadata: Dict[str, Any],
                                   element_frequency: Dict[str, Any], mapped_elements: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create template for specific page number with mixed content support"""
        
        if not pages:
            return None
        
        # Analyze content types on this page
        content_types = self._analyze_content_types_on_page(pages)
        
        # Infer page role and title
        page_role = self._infer_page_role_from_content(pages, page_num)
        page_title = self._infer_page_title_from_content(pages, page_num)
        
        # Create mixed content blocks
        template_blocks = self._create_mixed_content_blocks(pages, element_frequency, mapped_elements)
        
        # Determine if this page is required based on frequency
        total_docs = len(set(page['doc_id'] for page in pages))
        page_frequency = len(pages) / max(total_docs, 1)
        is_required = page_frequency >= 0.5
        
        return {
            "page_number": page_num,
            "page_title": page_title,
            "page_role": page_role,
            "content_types": content_types,
            "required": is_required,
            "frequency_percentage": round(page_frequency * 100, 1),
            "document_count": len(pages),
            "blocks": template_blocks
        }

    def _analyze_content_types_on_page(self, pages: List[Dict[str, Any]]) -> List[str]:
        """Analyze what types of content appear on this page number"""
        content_types = set()
        
        for page in pages:
            for element in page.get('elements', []):
                element_type = element.get('type', '').lower()
                
                if any(keyword in element_type for keyword in ['chart', 'graph']):
                    content_types.add('charts')
                elif element_type in ['title', 'subtitle', 'heading', 'sections_h1', 'subsections_h2']:
                    content_types.add('headings')
                elif element_type in ['paragraph', 'paragraphs', 'text', 'explanations']:
                    content_types.add('text')
                elif any(keyword in element_type for keyword in ['table', 'content_tables']):
                    content_types.add('tables')
                elif any(keyword in element_type for keyword in ['figure', 'image', 'diagram']):
                    content_types.add('figures')
                elif any(keyword in element_type for keyword in ['list', 'bullet', 'numbered']):
                    content_types.add('lists')
                elif element_type in ['executive_summary_text', 'executive_summary_key_points']:
                    content_types.add('summary')
        
        return sorted(list(content_types))

    def _infer_page_role_from_content(self, pages: List[Dict[str, Any]], page_num: int) -> str:
        """Infer the role/purpose of this page based on content"""
        
        # Analyze elements to determine page role
        element_types = []
        for page in pages:
            for element in page.get('elements', []):
                element_types.append(element.get('type', '').lower())
        
        element_counter = Counter(element_types)
        
        # Page 1 is usually cover/introduction
        if page_num == 1:
            return 'cover_introduction'
        
        # Determine role based on dominant content
        if any('executive_summary' in elem for elem in element_types):
            return 'executive_summary'
        elif any('chart' in elem or 'graph' in elem for elem in element_types):
            if any('financial' in elem or 'revenue' in elem for elem in element_types):
                return 'financial_analysis'
            else:
                return 'data_visualization'
        elif any('contact' in elem for elem in element_types):
            return 'contact_information'
        elif any('table' in elem for elem in element_types):
            return 'tabular_data'
        elif element_counter.get('paragraph', 0) > 2:
            return 'detailed_content'
        else:
            return 'mixed_content'

    def _infer_page_title_from_content(self, pages: List[Dict[str, Any]], page_num: int) -> str:
        """Infer appropriate title for this page based on content"""
        
        # Look for actual titles in the content
        titles = []
        for page in pages:
            for element in page.get('elements', []):
                if element.get('type') in ['title', 'heading', 'sections_h1']:
                    text = element.get('text', '')
                    if text and len(text) < 100:  # Reasonable title length
                        titles.append(text)
        
        if titles:
            # Use most common title
            title_counter = Counter(titles)
            return title_counter.most_common(1)[0][0]
        
        # Fallback to role-based titles
        role_titles = {
            'cover_introduction': 'Cover Page',
            'executive_summary': 'Executive Summary',
            'financial_analysis': 'Financial Analysis',
            'data_visualization': 'Performance Metrics',
            'contact_information': 'Contact Information',
            'tabular_data': 'Data Tables',
            'detailed_content': 'Detailed Information',
            'mixed_content': f'Page {page_num} Content'
        }
        
        page_role = self._infer_page_role_from_content(pages, page_num)
        return role_titles.get(page_role, f'Page {page_num}')

    def _create_mixed_content_blocks(self, pages: List[Dict[str, Any]], 
                                   element_frequency: Dict[str, Any], 
                                   mapped_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create blocks that can handle mixed content on same page"""
        
        # Collect all elements from this page number across documents
        all_elements = []
        for page in pages:
            all_elements.extend(page.get('elements', []))
        
        # Group by element type, not position
        element_groups = defaultdict(list)
        for element in all_elements:
            element_type = element.get('type', 'unknown')
            element_groups[element_type].append(element)
        
        # Create blocks for each element type found on this page
        blocks = []
        block_counter = 1
        
        for element_type, elements in element_groups.items():
            # Analyze this element pattern
            element_pattern = self._analyze_element_pattern(elements)
            
            # Create block using simplified method
            block = self._create_simple_template_block(
                element_type, block_counter, element_pattern, element_frequency
            )
            
            if block:
                blocks.append(block)
                block_counter += 1
        
        return blocks

    def _analyze_element_pattern(self, elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a group of elements with descriptions and enhanced chart/figure data"""
        
        # Get element types
        types = [elem.get('type') for elem in elements]
        most_common_type = Counter(types).most_common(1)[0][0]
        
        # Get text content and descriptions
        texts = []
        descriptions = []
        charts = []
        figures = []
        
        for elem in elements:
            # Extract descriptions
            if elem.get('description'):
                descriptions.append(elem['description'])
            
            # Extract text content
            if elem.get('text'):
                texts.append(elem['text'])
            elif elem.get('items'):
                texts.append(' '.join(elem['items']))
            
            # Extract chart data
            if elem.get('chart'):
                charts.append(elem['chart'])
            
            # Extract figure data
            if elem.get('figure'):
                figures.append(elem['figure'])
        
        # Determine if content is static or dynamic
        is_static = self._is_content_static(texts)
        
        # Check for PII
        pii_types = [elem.get('pii_type', 'NONE') for elem in elements]
        has_pii = any(pii != 'NONE' for pii in pii_types)
        
        # Get most common description
        element_description = ""
        if descriptions:
            element_description = Counter(descriptions).most_common(1)[0][0]
        
        return {
            'type': most_common_type,
            'description': element_description,
            'texts': texts,
            'charts': charts,
            'figures': figures,
            'is_static': is_static,
            'has_pii': has_pii,
            'pii_types': pii_types,
            'sample_element': elements[0] if elements else {}
        }

    def _create_simple_template_block(self, element_type: str, block_num: int, 
                                    element_pattern: Dict[str, Any], 
                                    element_frequency: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a simple template block with enhanced data"""
        
        is_static = element_pattern.get('is_static', False)
        has_pii = element_pattern.get('has_pii', False)
        texts = element_pattern.get('texts', [])
        description = element_pattern.get('description', '')
        charts = element_pattern.get('charts', [])
        figures = element_pattern.get('figures', [])
        
        # Skip empty blocks
        if not texts or all(not text.strip() for text in texts):
            return None
        
        block_id = f"page_block_{element_type}_{block_num}"
        
        # Get frequency info
        freq_info = element_frequency.get(element_type, {})
        doc_percentage = freq_info.get('document_percentage', 100)
        is_optional = doc_percentage < 70
        
        block = {
            "block_id": block_id,
            "type": element_type,
            "description": description,
            "content_mode": "static" if is_static else "dynamic",
            "optional": is_optional,
            "frequency_info": {
                "document_percentage": doc_percentage,
                "total_occurrences": freq_info.get('total_count', 1)
            },
            "static_text": None,
            "field_schema": None,
            "chart_data": charts[0] if charts else None,
            "figure_data": figures[0] if figures else None
        }
        
        if is_static and texts:
            # Use most common text
            text_counter = Counter(texts)
            most_common_text = text_counter.most_common(1)[0][0]
            block['static_text'] = most_common_text
        elif not is_static:
            # Create field schema
            block['field_schema'] = {
                'field_id': element_type,
                'label': element_type.replace('_', ' ').title(),
                'data_type': 'string',
                'required': not is_optional,
                'pii_type': element_pattern.get('pii_types', ['NONE'])[0]
            }
        
        return block

    def _is_content_static(self, texts: List[str]) -> bool:
        """Determine if content is static or dynamic based on similarity"""
        if len(texts) <= 1:
            return True
        
        # Simple similarity check
        first_text = texts[0].lower().strip()
        similar_count = sum(1 for text in texts[1:] if self._text_similarity(first_text, text.lower().strip()) > 0.8)
        
        return similar_count >= len(texts) * 0.7

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

    # Fallback methods for compatibility
    def _analyze_document_structure(self, per_page_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze document structure"""
        return {
            'total_documents': len(set(doc.get('doc_id') for doc in per_page_docs)),
            'total_pages': len(per_page_docs),
            'page_distribution': {}
        }

    def _identify_common_elements_with_catalog(self, per_page_docs: List[Dict[str, Any]], 
                                             mapped_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify common elements using catalog mapping - simplified version"""
        return []

    def _analyze_element_frequency_with_catalog(self, per_page_docs: List[Dict[str, Any]], 
                                              mapped_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze element frequency using catalog mapping - simplified version"""
        return {}

    def get_catalog_integration_summary(self) -> Dict[str, Any]:
        """Get summary of catalog integration capabilities"""
        return self.catalog.get_catalog_summary()
