#!/usr/bin/env python3
"""
Demo: Enhanced Master Template System
Shows the new description and chart/figure features
"""

import json
from catalog_integration import CatalogIntegration

def demo_enhanced_system():
    """Demonstrate the enhanced system with descriptions and chart/figure data"""
    
    print("🎯 Enhanced Master Template System Demo")
    print("=" * 60)
    
    # Initialize catalog
    print("\n📋 Loading Master Catalog...")
    catalog = CatalogIntegration()
    
    summary = catalog.get_catalog_summary()
    print(f"✅ Loaded: {summary['catalog_name']}")
    print(f"   • Version: {summary['version']}")
    print(f"   • Elements: {summary['total_elements']}")
    
    # Demo enhanced element detection
    print(f"\n🔍 Simulating Enhanced Document Analysis...")
    
    mock_detected_elements = [
        {
            'element_id': 'e1',
            'type': 'title',
            'text': 'TechCorp Annual Report 2024',
            'description': 'Main document title identifying the annual business report for stakeholders',
            'importance': 'critical',
            'category': 'document_identity_and_metadata',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e2',
            'type': 'executive_summary_text',
            'text': 'TechCorp achieved record growth in 2024...',
            'description': 'Executive summary highlighting key achievements, financial performance, and strategic initiatives for the year',
            'importance': 'critical',
            'category': 'front_matter',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e3',
            'type': 'charts_graphs',
            'text': 'Revenue Growth Chart',
            'description': 'Visual representation of quarterly revenue growth showing consistent upward trend',
            'chart': {
                'chart_type': 'line',
                'title': 'Quarterly Revenue Growth 2024',
                'description': 'Shows 35% year-over-year revenue growth with strong Q4 performance',
                'data': [
                    {'name': 'Q1 2024', 'value': '25.2M', 'unit': 'USD'},
                    {'name': 'Q2 2024', 'value': '28.7M', 'unit': 'USD'},
                    {'name': 'Q3 2024', 'value': '32.1M', 'unit': 'USD'},
                    {'name': 'Q4 2024', 'value': '38.5M', 'unit': 'USD'}
                ],
                'source': 'Finance Department'
            },
            'importance': 'important',
            'category': 'supporting_elements',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e4',
            'type': 'figures_images',
            'text': 'Market Share Analysis',
            'description': 'Infographic showing company market position and competitive landscape analysis',
            'figure': {
                'figure_type': 'infographic',
                'title': 'Market Position 2024',
                'description': 'Comprehensive market share analysis across key business segments',
                'elements': [
                    {'name': 'Cloud Services', 'value': '23% market share'},
                    {'name': 'AI Solutions', 'value': '18% market share'},
                    {'name': 'Data Analytics', 'value': '31% market share'},
                    {'name': 'Cybersecurity', 'value': '15% market share'}
                ]
            },
            'importance': 'important',
            'category': 'analysis_and_findings',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e5',
            'type': 'contact_email',
            'text': 'investor.relations@techcorp.com',
            'description': 'Primary email contact for investor inquiries and shareholder communications',
            'importance': 'optional',
            'category': 'end_matter',
            'pii_type': 'EMAIL'
        }
    ]
    
    print(f"   📄 Detected {len(mock_detected_elements)} enhanced elements")
    
    # Show enhanced element details
    print(f"\n📊 Enhanced Element Details:")
    for elem in mock_detected_elements:
        print(f"\n   🔍 **{elem['type']}** ({elem['category']})")
        print(f"      💡 Description: {elem['description']}")
        
        if 'chart' in elem:
            chart = elem['chart']
            print(f"      📊 Chart: {chart['title']} ({chart['chart_type']})")
            print(f"         📝 {chart['description']}")
            print(f"         📈 Data Points: {len(chart['data'])}")
            for data_point in chart['data'][:2]:  # Show first 2
                print(f"            • {data_point['name']}: {data_point['value']} {data_point['unit']}")
            if len(chart['data']) > 2:
                print(f"            • ... and {len(chart['data']) - 2} more")
        
        if 'figure' in elem:
            figure = elem['figure']
            print(f"      🖼️ Figure: {figure['title']} ({figure['figure_type']})")
            print(f"         📝 {figure['description']}")
            print(f"         🔍 Elements: {len(figure['elements'])}")
            for element in figure['elements'][:2]:  # Show first 2
                print(f"            • {element['name']}: {element['value']}")
            if len(figure['elements']) > 2:
                print(f"            • ... and {len(figure['elements']) - 2} more")
        
        if elem['pii_type'] != 'NONE':
            print(f"      🔒 PII Type: {elem['pii_type']}")
    
    # Map elements to catalog
    print(f"\n🔗 Mapping Enhanced Elements to Catalog...")
    mapped_elements = catalog.map_detected_elements(mock_detected_elements)
    
    mapped_count = len([e for e in mapped_elements if e['mapping_status'] == 'mapped'])
    unmapped_count = len([e for e in mapped_elements if e['mapping_status'] == 'unmapped'])
    
    print(f"   ✅ Mapped to catalog: {mapped_count}")
    print(f"   ⚠️ Custom elements: {unmapped_count}")
    
    # Generate enhanced template
    print(f"\n🧠 Generating Enhanced Master Template...")
    
    # Create mock element frequency data
    element_frequency = {}
    for mapped_elem in mapped_elements:
        field_id = mapped_elem['field_schema']['field_id']
        element_frequency[field_id] = {
            'total_count': 1,
            'document_count': 1,
            'document_percentage': 100.0,
            'is_static': False
        }
    
    template = catalog.generate_catalog_based_template(mapped_elements, element_frequency)
    
    # Enhance template with mock page structure
    enhanced_template = {
        "template_id": "enhanced_catalog_master_v1",
        "name": "Enhanced Catalog Master Template with Descriptions",
        "description": "Advanced template with element descriptions and structured chart/figure data",
        "doc_type": "comprehensive_business_document",
        "output_format": "pptx",
        "catalog_integration": template.get('catalog_integration', {}),
        "enhancement_features": {
            "element_descriptions": True,
            "structured_chart_data": True,
            "structured_figure_data": True,
            "pii_detection": True
        },
        "pages": [
            {
                "page_type": "cover",
                "title": "Cover Page",
                "required": True,
                "blocks": [
                    {
                        "block_id": "cover_title_1",
                        "type": "title",
                        "description": "Main document title identifying the annual business report for stakeholders",
                        "content_mode": "dynamic",
                        "catalog_mapped": True,
                        "field_schema": {
                            "field_id": "title",
                            "data_type": "string",
                            "pii_type": "NONE"
                        }
                    }
                ]
            },
            {
                "page_type": "executive_summary",
                "title": "Executive Summary",
                "required": True,
                "blocks": [
                    {
                        "block_id": "exec_summary_1",
                        "type": "executive_summary_text",
                        "description": "Executive summary highlighting key achievements, financial performance, and strategic initiatives for the year",
                        "content_mode": "dynamic",
                        "catalog_mapped": True,
                        "field_schema": {
                            "field_id": "executive_summary_text",
                            "data_type": "rich_text",
                            "pii_type": "NONE"
                        }
                    }
                ]
            },
            {
                "page_type": "financial_metrics",
                "title": "Financial Performance",
                "required": True,
                "blocks": [
                    {
                        "block_id": "financial_chart_1",
                        "type": "charts_graphs",
                        "description": "Visual representation of quarterly revenue growth showing consistent upward trend",
                        "content_mode": "dynamic",
                        "catalog_mapped": True,
                        "chart_data": {
                            "chart_type": "line",
                            "title": "Quarterly Revenue Growth 2024",
                            "description": "Shows 35% year-over-year revenue growth with strong Q4 performance",
                            "data": [
                                {"name": "Q1 2024", "value": "25.2M", "unit": "USD"},
                                {"name": "Q2 2024", "value": "28.7M", "unit": "USD"},
                                {"name": "Q3 2024", "value": "32.1M", "unit": "USD"},
                                {"name": "Q4 2024", "value": "38.5M", "unit": "USD"}
                            ],
                            "source": "Finance Department"
                        }
                    }
                ]
            },
            {
                "page_type": "market_analysis",
                "title": "Market Analysis",
                "required": True,
                "blocks": [
                    {
                        "block_id": "market_figure_1",
                        "type": "figures_images",
                        "description": "Infographic showing company market position and competitive landscape analysis",
                        "content_mode": "dynamic",
                        "catalog_mapped": True,
                        "figure_data": {
                            "figure_type": "infographic",
                            "title": "Market Position 2024",
                            "description": "Comprehensive market share analysis across key business segments",
                            "elements": [
                                {"name": "Cloud Services", "value": "23% market share"},
                                {"name": "AI Solutions", "value": "18% market share"},
                                {"name": "Data Analytics", "value": "31% market share"},
                                {"name": "Cybersecurity", "value": "15% market share"}
                            ]
                        }
                    }
                ]
            },
            {
                "page_type": "contact",
                "title": "Contact Information",
                "required": False,
                "blocks": [
                    {
                        "block_id": "contact_email_1",
                        "type": "contact_email",
                        "description": "Primary email contact for investor inquiries and shareholder communications",
                        "content_mode": "dynamic",
                        "catalog_mapped": False,
                        "field_schema": {
                            "field_id": "contact_email",
                            "data_type": "string",
                            "pii_type": "EMAIL"
                        }
                    }
                ]
            }
        ]
    }
    
    print(f"   ✅ Generated: {enhanced_template['name']}")
    print(f"   • Template ID: {enhanced_template['template_id']}")
    print(f"   • Pages: {len(enhanced_template['pages'])}")
    print(f"   • Enhancement Features: {list(enhanced_template['enhancement_features'].keys())}")
    
    # Show enhanced template structure
    print(f"\n🎯 Enhanced Template Structure:")
    for page in enhanced_template['pages']:
        print(f"\n   📄 **{page['page_type'].upper()}** - {page['title']}")
        print(f"      Required: {'✅' if page['required'] else '🟡'}")
        
        for block in page['blocks']:
            print(f"      🔹 {block['type']}")
            print(f"         💡 {block['description']}")
            
            if block.get('chart_data'):
                chart = block['chart_data']
                print(f"         📊 Chart: {chart['title']} ({len(chart['data'])} data points)")
            
            if block.get('figure_data'):
                figure = block['figure_data']
                print(f"         🖼️ Figure: {figure['title']} ({len(figure['elements'])} elements)")
            
            if block.get('field_schema', {}).get('pii_type', 'NONE') != 'NONE':
                print(f"         🔒 PII: {block['field_schema']['pii_type']}")
    
    # Save enhanced template
    output_file = 'enhanced_master_template_demo.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_template, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Enhanced template saved to: {output_file}")
    print(f"📏 File size: {len(json.dumps(enhanced_template))} characters")
    
    print(f"\n🎉 Enhanced System Demo Complete!")
    print(f"   The system now provides:")
    print(f"   ✅ Detailed element descriptions from LLM")
    print(f"   ✅ Structured chart data with name-value pairs")
    print(f"   ✅ Structured figure data with element breakdowns")
    print(f"   ✅ Enhanced PII detection and handling")
    print(f"   ✅ Rich template output for immediate use")
    
    return enhanced_template

if __name__ == "__main__":
    demo_enhanced_system()
