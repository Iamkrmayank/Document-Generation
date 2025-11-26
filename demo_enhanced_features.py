#!/usr/bin/env python3
"""
Demo script showcasing the enhanced template inference features
"""

import json
from template_inference import TemplateInferenceEngine

def create_complex_mock_data():
    """Create mock data that demonstrates edge cases and advanced features"""
    
    return [
        # Document 1: Standard structure (10 pages)
        {
            "doc_id": "doc_1",
            "page_index": 1,
            "elements": [
                {"element_id": "e1", "type": "title", "text": "Acme Health Inc.", "pii_type": "ORG_NAME"},
                {"element_id": "e2", "type": "subtitle", "text": "Healthcare Innovation", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_1", 
            "page_index": 2,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "About Us", "pii_type": "NONE"},
                {"element_id": "e2", "type": "paragraph", "text": "Acme Health Inc. is a leading healthcare technology company.", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 8,  # Services page appears later
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Our Services", "pii_type": "NONE"},
                {"element_id": "e2", "type": "bullet_list", "items": ["Telemedicine", "AI Diagnostics", "Health Analytics"], "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 10,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Contact Us", "pii_type": "NONE"},
                {"element_id": "e2", "type": "paragraph", "text": "Email: contact@acmehealth.com Phone: (555) 123-4567", "pii_type": "EMAIL"}
            ]
        },
        
        # Document 2: Different structure (8 pages, different order)
        {
            "doc_id": "doc_2",
            "page_index": 1,
            "elements": [
                {"element_id": "e1", "type": "title", "text": "TechFlow Solutions Ltd", "pii_type": "ORG_NAME"},
                {"element_id": "e2", "type": "subtitle", "text": "Digital Transformation Experts", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 3,  # About page appears later
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Who We Are", "pii_type": "NONE"},  # Different heading, same semantic meaning
                {"element_id": "e2", "type": "paragraph", "text": "TechFlow Solutions provides cutting-edge digital transformation services.", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 2,  # Services page appears earlier
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "What We Do", "pii_type": "NONE"},  # Different heading, same semantic meaning
                {"element_id": "e2", "type": "bullet_list", "items": ["Cloud Migration", "Process Automation", "Data Analytics"], "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 6,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Our Team", "pii_type": "NONE"},
                {"element_id": "e2", "type": "paragraph", "text": "Led by industry experts with 20+ years experience.", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 8,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Get In Touch", "pii_type": "NONE"},  # Different heading, same semantic meaning
                {"element_id": "e2", "type": "paragraph", "text": "info@techflow.com | +1-800-TECH-FLOW", "pii_type": "EMAIL"}
            ]
        },
        
        # Document 3: Shorter structure (5 pages) with unique page
        {
            "doc_id": "doc_3",
            "page_index": 1,
            "elements": [
                {"element_id": "e1", "type": "title", "text": "InnovateTech Corp", "pii_type": "ORG_NAME"}
            ]
        },
        {
            "doc_id": "doc_3",
            "page_index": 2,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Company Overview", "pii_type": "NONE"},  # Different heading, same semantic meaning
                {"element_id": "e2", "type": "paragraph", "text": "InnovateTech Corp specializes in AI and machine learning solutions.", "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_3",
            "page_index": 3,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Awards & Recognition", "pii_type": "NONE"},  # Unique page type
                {"element_id": "e2", "type": "bullet_list", "items": ["Best AI Startup 2023", "Innovation Award 2022"], "pii_type": "NONE"}
            ]
        },
        {
            "doc_id": "doc_3",
            "page_index": 4,
            "elements": [
                {"element_id": "e1", "type": "heading", "text": "Solutions", "pii_type": "NONE"},
                {"element_id": "e2", "type": "bullet_list", "items": ["Machine Learning Platforms", "Predictive Analytics", "Computer Vision"], "pii_type": "NONE"}
            ]
        }
    ]

def demo_enhanced_features():
    """Demonstrate the enhanced template inference capabilities"""
    
    print("🚀 Enhanced Template Inference Demo")
    print("=" * 50)
    
    # Create mock bedrock client
    class MockBedrockClient:
        pass
    
    mock_client = MockBedrockClient()
    engine = TemplateInferenceEngine(mock_client)
    
    # Create complex mock data
    mock_data = create_complex_mock_data()
    
    print(f"📊 Input: {len(mock_data)} pages from 3 documents with different structures")
    print("   - Doc 1: 4 pages (standard order)")
    print("   - Doc 2: 5 pages (different order)")  
    print("   - Doc 3: 4 pages (shorter, with unique 'awards' page)")
    print()
    
    # Generate template
    template = engine.infer_master_template(mock_data)
    
    # Analyze results
    print("📋 Template Analysis:")
    print(f"   - Total pages in template: {len(template['pages'])}")
    print(f"   - Global document fields: {len(template['document_fields'])}")
    print()
    
    # Show semantic grouping
    print("🔍 Semantic Page Classification:")
    for page in template['pages']:
        required_status = "Required" if page['required'] else "Optional"
        print(f"   - {page['page_type'].upper()}: '{page['title']}' ({required_status})")
    print()
    
    # Show global fields
    print("🌐 Global Document Fields:")
    for field in template['document_fields']:
        pii_info = f" [{field['pii_type']}]" if field['pii_type'] != 'NONE' else ""
        print(f"   - {field['field_id']}: {field['label']}{pii_info}")
    print()
    
    # Show static vs dynamic content
    print("📝 Content Analysis:")
    for page in template['pages']:
        static_blocks = [b for b in page['blocks'] if b['content_mode'] == 'static']
        dynamic_blocks = [b for b in page['blocks'] if b['content_mode'] == 'dynamic']
        print(f"   - {page['page_type'].upper()}: {len(static_blocks)} static, {len(dynamic_blocks)} dynamic blocks")
    print()
    
    # Show PII handling
    print("🔒 PII Detection & Sanitization:")
    pii_fields = [f for f in template['document_fields'] if f['pii_type'] != 'NONE']
    if pii_fields:
        for field in pii_fields:
            print(f"   - {field['field_id']}: {field['pii_type']} (sanitized)")
    else:
        print("   - No PII detected in global fields")
    print()
    
    # Show canonical ordering
    print("📑 Canonical Page Ordering:")
    for i, page in enumerate(template['pages'], 1):
        print(f"   {i}. {page['page_type']} (index: {page['page_index']})")
    print()
    
    # Export sample
    output_file = "demo_template_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Full template saved to: {output_file}")
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    demo_enhanced_features()
