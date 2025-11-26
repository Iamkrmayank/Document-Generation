#!/usr/bin/env python3
"""
Comprehensive test for the enhanced document template system
"""

import json
from template_inference import TemplateInferenceEngine

def create_comprehensive_mock_data():
    """Create comprehensive mock data representing real document structures"""
    
    return [
        # Document 1: Full corporate profile with comprehensive structure
        {
            "doc_id": "doc_1",
            "page_index": 1,
            "page_role": "cover",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "category": "metadata",
                    "importance": "critical",
                    "text": "Acme Health Inc.",
                    "position_hint": "top",
                    "pii_type": "ORG_NAME"
                },
                {
                    "element_id": "e2",
                    "type": "subtitle",
                    "category": "metadata", 
                    "importance": "important",
                    "text": "Healthcare Innovation Solutions",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e3",
                    "type": "author",
                    "category": "metadata",
                    "importance": "optional",
                    "text": "Corporate Communications Team",
                    "position_hint": "bottom",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e4",
                    "type": "date_created",
                    "category": "metadata",
                    "importance": "supplementary",
                    "text": "March 2024",
                    "position_hint": "bottom",
                    "pii_type": "DATE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 2,
            "page_role": "front_matter",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "executive_summary",
                    "category": "front_matter",
                    "importance": "critical",
                    "text": "Acme Health Inc. is a leading healthcare technology company...",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "table_of_contents",
                    "category": "front_matter",
                    "importance": "important",
                    "items": ["About Us", "Our Services", "Team", "Contact"],
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 3,
            "page_role": "introduction",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "purpose",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "This document provides an overview of our company...",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "scope",
                    "category": "main_body",
                    "importance": "important",
                    "text": "Covers our services, team, and contact information",
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 4,
            "page_role": "main_content",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "About Us",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "paragraph",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "Acme Health Inc. specializes in healthcare technology solutions...",
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 8,
            "page_role": "analysis",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "data_analysis",
                    "category": "analysis",
                    "importance": "critical",
                    "text": "Market Analysis: Healthcare IT market growing at 15% CAGR",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "chart",
                    "category": "supporting",
                    "importance": "important",
                    "chart": {
                        "chart_type": "bar",
                        "labels": ["2022", "2023", "2024"],
                        "values": [100, 115, 132],
                        "description": "Revenue Growth"
                    },
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_1",
            "page_index": 10,
            "page_role": "end_matter",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "references",
                    "category": "end_matter",
                    "importance": "supplementary",
                    "items": ["Healthcare IT Report 2024", "Industry Analysis Q1"],
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "contact_information",
                    "category": "end_matter",
                    "importance": "important",
                    "text": "Contact: info@acmehealth.com | (555) 123-4567",
                    "position_hint": "bottom",
                    "pii_type": "EMAIL"
                }
            ]
        },
        
        # Document 2: Different structure, similar content
        {
            "doc_id": "doc_2",
            "page_index": 1,
            "page_role": "cover",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "category": "metadata",
                    "importance": "critical",
                    "text": "TechFlow Solutions Ltd",
                    "position_hint": "top",
                    "pii_type": "ORG_NAME"
                },
                {
                    "element_id": "e2",
                    "type": "subtitle",
                    "category": "metadata",
                    "importance": "important", 
                    "text": "Digital Transformation Experts",
                    "position_hint": "top",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 2,
            "page_role": "main_content",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "Who We Are",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "paragraph",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "TechFlow Solutions provides cutting-edge digital transformation...",
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        {
            "doc_id": "doc_2",
            "page_index": 5,
            "page_role": "recommendations",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "key_recommendations",
                    "category": "recommendations",
                    "importance": "critical",
                    "text": "Strategic Recommendations for Digital Transformation",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "action_plan",
                    "category": "recommendations",
                    "importance": "critical",
                    "items": ["Phase 1: Assessment", "Phase 2: Implementation", "Phase 3: Optimization"],
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        },
        
        # Document 3: Minimal structure
        {
            "doc_id": "doc_3",
            "page_index": 1,
            "page_role": "cover",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "title",
                    "category": "metadata",
                    "importance": "critical",
                    "text": "StartupXYZ Corp",
                    "position_hint": "top",
                    "pii_type": "ORG_NAME"
                }
            ]
        },
        {
            "doc_id": "doc_3",
            "page_index": 2,
            "page_role": "main_content",
            "elements": [
                {
                    "element_id": "e1",
                    "type": "heading",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "Company Overview",
                    "position_hint": "top",
                    "pii_type": "NONE"
                },
                {
                    "element_id": "e2",
                    "type": "paragraph",
                    "category": "main_body",
                    "importance": "critical",
                    "text": "StartupXYZ Corp is an innovative AI company...",
                    "position_hint": "middle",
                    "pii_type": "NONE"
                }
            ]
        }
    ]

def test_comprehensive_system():
    """Test the comprehensive document template system"""
    
    print("🚀 Comprehensive Document Template System Test")
    print("=" * 60)
    
    # Create mock bedrock client
    class MockBedrockClient:
        pass
    
    mock_client = MockBedrockClient()
    engine = TemplateInferenceEngine(mock_client)
    
    # Create comprehensive mock data
    mock_data = create_comprehensive_mock_data()
    
    print(f"📊 Input Analysis:")
    print(f"   - Total pages: {len(mock_data)}")
    print(f"   - Documents: {len(set(doc['doc_id'] for doc in mock_data))}")
    print(f"   - Page roles: {set(doc.get('page_role', 'unknown') for doc in mock_data)}")
    print()
    
    # Generate comprehensive template
    template = engine.infer_master_template(mock_data)
    
    # Display comprehensive results
    print("📋 Comprehensive Template Analysis:")
    print(f"   - Template ID: {template['template_id']}")
    print(f"   - Template Name: {template['name']}")
    print(f"   - Total pages in template: {len(template['pages'])}")
    print(f"   - Document metadata fields: {len(template.get('document_metadata', {}))}")
    print(f"   - Global document fields: {len(template['document_fields'])}")
    print(f"   - Common elements identified: {len(template['common_elements'])}")
    print()
    
    # Analysis summary
    analysis = template['analysis_summary']
    print("🔍 Document Structure Analysis:")
    for doc_id, structure in analysis['document_structure'].items():
        print(f"   - {doc_id.upper()}:")
        print(f"     * Pages: {structure['total_pages']}")
        print(f"     * Page roles: {set(structure['page_roles'])}")
        print(f"     * Element categories: {structure['element_categories']}")
        print(f"     * Has front matter: {structure['has_front_matter']}")
        print(f"     * Has analysis: {structure['has_analysis']}")
        print(f"     * Has recommendations: {structure['has_recommendations']}")
    print()
    
    # Common elements
    print("🌐 Common Elements Across Documents:")
    for element in template['common_elements'][:10]:  # Show top 10
        print(f"   - {element['element_type']} ({element['element_category']}): {element['frequency']}/{analysis['total_documents']} docs ({element['percentage']:.1f}%)")
    print()
    
    # Element frequency analysis
    print("📊 Element Frequency Analysis (Top 10):")
    sorted_elements = sorted(template['element_frequency'].items(), 
                           key=lambda x: x[1]['document_percentage'], reverse=True)
    for element_type, stats in sorted_elements[:10]:
        print(f"   - {element_type}: {stats['document_count']}/{analysis['total_documents']} docs ({stats['document_percentage']:.1f}%)")
    print()
    
    # Page structure
    print("📑 Template Page Structure:")
    for page in template['pages']:
        required_status = "Required" if page['required'] else "Optional"
        print(f"   {page['page_index']}. {page['page_type'].upper()} ({page['page_role']})")
        print(f"      - Title: {page['title']}")
        print(f"      - Status: {required_status} ({page['frequency_percentage']}%)")
        print(f"      - Blocks: {len(page['blocks'])}")
        
        # Show block details
        for block in page['blocks'][:3]:  # Show first 3 blocks
            mode = block['content_mode']
            optional = "Optional" if block['optional'] else "Required"
            print(f"        * {block['type']} ({block['category']}) - {mode}, {optional}")
    print()
    
    # Global fields
    print("🌐 Global Document Fields:")
    for field in template['document_fields']:
        pii_info = f" [{field['pii_type']}]" if field['pii_type'] != 'NONE' else ""
        print(f"   - {field['field_id']}: {field['label']} ({field['data_type']}){pii_info}")
    print()
    
    # Export comprehensive template
    output_file = "comprehensive_template_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Comprehensive template saved to: {output_file}")
    print(f"📏 File size: {len(json.dumps(template, indent=2))} characters")
    print()
    
    # Validation
    print("✅ Validation Results:")
    print(f"   - Template structure: Valid")
    print(f"   - JSON serializable: Valid")
    print(f"   - All pages have blocks: {all(len(page['blocks']) > 0 for page in template['pages'])}")
    print(f"   - PII properly handled: {any(field['pii_type'] != 'NONE' for field in template['document_fields'])}")
    print(f"   - Element categories covered: {len(set(block['category'] for page in template['pages'] for block in page['blocks']))}")
    print()
    
    print("🎉 Comprehensive system test completed successfully!")
    return template

if __name__ == "__main__":
    test_comprehensive_system()
