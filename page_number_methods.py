# Page number-based methods to add to template_inference.py

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
        
        # Create block using existing method
        block = self._create_comprehensive_template_block(
            f"page_content", block_counter, element_pattern, {}, {}, element_frequency
        )
        
        if block:
            # Update block ID to be more descriptive
            block['block_id'] = f"page_block_{element_type}_{block_counter}"
            blocks.append(block)
            block_counter += 1
    
    return blocks
