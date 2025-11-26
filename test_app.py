#!/usr/bin/env python3
"""
Test script for the Master Template Generator application
"""

import json
from typing import Dict, Any

def test_template_inference():
    """Test the enhanced template inference logic with comprehensive mock data"""
    
    # Mock page data simulating different document structures and page orders
    mock_page_data = [
        # Document 1: Standard order
        {
            "doc_id": "doc_1",
            "page_index": 1,
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "text": "Acme Corp",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "ORG_NAME"
                },
                {
                    "element_id": "e2",
                    "type": "subtitle",
                    "text": "Leading Innovation",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 2,
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "text": "About Us",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "paragraph",
                    "text": "Acme Corp is a leading technology company specializing in innovative solutions.",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                }
            ]
        },
        # Document 2: Different order, same semantic content
        {
            "doc_id": "doc_2",
            "page_index": 1,
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "text": "TechFlow Solutions",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "ORG_NAME"
                },
                {
                    "element_id": "e2",
                    "type": "subtitle",
                    "text": "Digital Transformation Experts",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 3,  # Different page index but same semantic content
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "text": "About the Company",  # Similar but not identical heading
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "paragraph",
                    "text": "TechFlow Solutions provides cutting-edge digital transformation services.",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                }
            ]
        },
        # Document 3: Additional page type
        {
            "doc_id": "doc_3",
            "page_index": 1,
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "text": "InnovateTech Inc",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "ORG_NAME"
                }
            ]
        },
        {
            "doc_id": "doc_3",
            "page_index": 2,
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "text": "Our Services",
                    "items": [],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "bullet_list",
                    "text": "",
                    "items": ["Cloud Solutions", "AI Development", "Data Analytics"],
                    "table": {},
                    "chart": {},
                    "position_hint": None,
                    "pii_type": "NONE"
                }
            ]
        }
    ]
    
    # Test template inference without AWS dependency
    from template_inference import TemplateInferenceEngine
    
    # Create a mock bedrock client
    class MockBedrockClient:
        pass
    
    mock_client = MockBedrockClient()
    engine = TemplateInferenceEngine(mock_client)
    
    # Test the inference
    template = engine.infer_master_template(mock_page_data)
    
    # Validate the enhanced output
    assert template["template_id"] == "catalog_integrated_master_v1"
    assert template["name"] == "Catalog-Integrated Master Template"
    assert len(template["pages"]) > 0
    
    # Check semantic page grouping (not index-based)
    page_types = [page["page_type"] for page in template["pages"]]
    assert "cover" in page_types
    assert "about" in page_types
    
    # Check canonical ordering
    cover_page = next(page for page in template["pages"] if page["page_type"] == "cover")
    about_page = next(page for page in template["pages"] if page["page_type"] == "about")
    assert cover_page["page_index"] < about_page["page_index"]
    
    # Check document fields for global elements
    field_ids = [field["field_id"] for field in template["document_fields"]]
    assert "company_name" in field_ids  # Should be global due to ORG_NAME PII type
    
    # Check static vs dynamic content detection
    cover_blocks = cover_page["blocks"]
    title_block = next((block for block in cover_blocks if block["type"] == "title"), None)
    assert title_block is not None
    assert title_block["content_mode"] == "dynamic"  # Company names vary
    assert title_block["field_schema"]["pii_type"] == "ORG_NAME"
    
    print("✅ Enhanced template inference test passed!")
    print(f"Generated template with {len(template['pages'])} pages")
    print(f"Page types: {page_types}")
    print(f"Document fields: {len(template['document_fields'])}")
    print(f"Global field IDs: {field_ids}")
    
    return template

def test_document_parser():
    """Test document parser initialization"""
    
    from parsing import DocumentParser
    
    parser = DocumentParser()
    print("✅ Document parser initialized successfully!")
    
    return parser

def main():
    """Run all tests"""
    
    print("🧪 Running Master Template Generator Tests\n")
    
    try:
        # Test 1: Document Parser
        print("Test 1: Document Parser")
        test_document_parser()
        print()
        
        # Test 2: Template Inference
        print("Test 2: Template Inference Engine")
        template = test_template_inference()
        print()
        
        # Test 3: JSON Serialization
        print("Test 3: JSON Serialization")
        json_output = json.dumps(template, indent=2)
        assert len(json_output) > 0
        print("✅ JSON serialization test passed!")
        print()
        
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo run the Streamlit app:")
        print("streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
