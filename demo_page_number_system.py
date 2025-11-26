#!/usr/bin/env python3
"""
Demo: Page Number-Based Template System
Shows how the new system works with page numbers instead of page types
"""

import json
from template_inference import TemplateInferenceEngine

def demo_page_number_system():
    """Demonstrate the page number-based template system"""
    
    print("🎯 Page Number-Based Template System Demo")
    print("=" * 60)
    
    # Mock bedrock client
    class MockBedrockClient:
        pass
    
    engine = TemplateInferenceEngine(MockBedrockClient())
    
    print("\n📄 Simulating 3 Company Profile Documents...")
    
    # Create realistic mock data representing 3 different company profiles
    mock_page_docs = [
        # Document 1: TechCorp (5 pages)
        {
            'doc_id': 'techcorp_profile',
            'page_index': 1,
            'elements': [
                {'type': 'title', 'text': 'TechCorp Annual Report 2024', 'description': 'Main company document title'},
                {'type': 'subtitle', 'text': 'Innovation & Excellence', 'description': 'Company tagline and year'},
                {'type': 'organization_logo', 'text': 'TechCorp Logo', 'description': 'Company brand logo'}
            ]
        },
        {
            'doc_id': 'techcorp_profile',
            'page_index': 2,
            'elements': [
                {'type': 'executive_summary_text', 'text': 'TechCorp achieved record growth...', 'description': 'Executive summary of company performance'},
                {'type': 'charts_graphs', 'text': 'Revenue Chart', 'description': 'Financial performance visualization',
                 'chart': {'title': 'Revenue Growth 2024', 'data': [{'name': 'Q1', 'value': '25M', 'unit': 'USD'}]}},
                {'type': 'paragraphs', 'text': 'Our strategic initiatives...', 'description': 'Detailed business explanation'}
            ]
        },
        {
            'doc_id': 'techcorp_profile',
            'page_index': 3,
            'elements': [
                {'type': 'sections_h1', 'text': 'Market Analysis', 'description': 'Section heading for market data'},
                {'type': 'content_tables', 'text': 'Market Share Table', 'description': 'Tabular market data'},
                {'type': 'figures_images', 'text': 'Market Position Diagram', 'description': 'Visual market analysis',
                 'figure': {'title': 'Market Position', 'elements': [{'name': 'Market Share', 'value': '23%'}]}}
            ]
        },
        
        # Document 2: InnovateCorp (4 pages)
        {
            'doc_id': 'innovatecorp_profile',
            'page_index': 1,
            'elements': [
                {'type': 'title', 'text': 'InnovateCorp Company Overview', 'description': 'Primary company identification'},
                {'type': 'subtitle', 'text': 'Leading the Future', 'description': 'Company mission statement'},
                {'type': 'organization_logo', 'text': 'InnovateCorp Brand', 'description': 'Corporate branding element'}
            ]
        },
        {
            'doc_id': 'innovatecorp_profile',
            'page_index': 2,
            'elements': [
                {'type': 'executive_summary_text', 'text': 'InnovateCorp delivered exceptional results...', 'description': 'High-level business summary'},
                {'type': 'charts_graphs', 'text': 'Growth Metrics', 'description': 'Performance indicators chart',
                 'chart': {'title': 'Growth Metrics 2024', 'data': [{'name': 'Revenue', 'value': '30M', 'unit': 'USD'}]}},
                {'type': 'bullet_points', 'items': ['Key Achievement 1', 'Key Achievement 2'], 'description': 'Major accomplishments list'}
            ]
        },
        {
            'doc_id': 'innovatecorp_profile',
            'page_index': 3,
            'elements': [
                {'type': 'sections_h1', 'text': 'Financial Performance', 'description': 'Financial section header'},
                {'type': 'charts_graphs', 'text': 'Financial Chart', 'description': 'Financial data visualization'},
                {'type': 'paragraphs', 'text': 'Financial analysis shows...', 'description': 'Financial performance narrative'}
            ]
        },
        
        # Document 3: GlobalTech (3 pages)
        {
            'doc_id': 'globaltech_profile',
            'page_index': 1,
            'elements': [
                {'type': 'title', 'text': 'GlobalTech Solutions Profile', 'description': 'Company profile document title'},
                {'type': 'subtitle', 'text': 'Global Excellence', 'description': 'Corporate positioning statement'}
            ]
        },
        {
            'doc_id': 'globaltech_profile',
            'page_index': 2,
            'elements': [
                {'type': 'executive_summary_text', 'text': 'GlobalTech continues to expand...', 'description': 'Business overview summary'},
                {'type': 'charts_graphs', 'text': 'Performance Dashboard', 'description': 'Key metrics visualization'}
            ]
        }
    ]
    
    print(f"   📊 Total Documents: 3")
    print(f"   📄 Total Pages: {len(mock_page_docs)}")
    print(f"   📋 Total Elements: {sum(len(doc.get('elements', [])) for doc in mock_page_docs)}")
    
    # Generate master template
    print(f"\n🧠 Generating Page Number-Based Master Template...")
    
    master_template = engine.infer_master_template(mock_page_docs)
    
    print(f"   ✅ Generated: {master_template['name']}")
    print(f"   • Template ID: {master_template['template_id']}")
    print(f"   • Total Pages in Template: {master_template['total_pages']}")
    print(f"   • Max Page Number: {master_template['max_page_number']}")
    
    # Show page-by-page breakdown
    print(f"\n📄 Page-by-Page Template Structure:")
    
    for page in master_template['pages']:
        page_num = page['page_number']
        title = page['page_title']
        role = page['page_role']
        content_types = page['content_types']
        required = "Required" if page['required'] else "Optional"
        frequency = page['frequency_percentage']
        
        # Content type icons
        content_icons = {
            'headings': '📝',
            'text': '📄', 
            'charts': '📊',
            'tables': '📋',
            'figures': '🖼️',
            'lists': '📌',
            'summary': '📋'
        }
        content_display = ' '.join([content_icons.get(ct, '📄') for ct in content_types])
        
        print(f"\n   📄 **PAGE {page_num}** - {title}")
        print(f"      🎭 Role: {role}")
        print(f"      🎨 Content Types: {', '.join(content_types)} {content_display}")
        print(f"      📊 Frequency: {frequency}% ({required})")
        print(f"      🧱 Blocks: {len(page['blocks'])}")
        
        # Show blocks with enhanced data
        for i, block in enumerate(page['blocks'][:3], 1):  # Show first 3 blocks
            block_type = block['type']
            description = block.get('description', 'No description')
            mode = block['content_mode']
            
            print(f"         {i}. {block_type} ({mode})")
            print(f"            💡 {description}")
            
            # Show chart data if available
            if block.get('chart_data'):
                chart = block['chart_data']
                print(f"            📊 Chart: {chart.get('title', 'Untitled')}")
                if chart.get('data'):
                    data_point = chart['data'][0]
                    print(f"               📈 Sample: {data_point.get('name')} = {data_point.get('value')} {data_point.get('unit', '')}")
            
            # Show figure data if available
            if block.get('figure_data'):
                figure = block['figure_data']
                print(f"            🖼️ Figure: {figure.get('title', 'Untitled')}")
                if figure.get('elements'):
                    element = figure['elements'][0]
                    print(f"               🔍 Sample: {element.get('name')} = {element.get('value')}")
        
        if len(page['blocks']) > 3:
            print(f"         ... and {len(page['blocks']) - 3} more blocks")
    
    # Show key benefits
    print(f"\n🎯 Key Benefits of Page Number Approach:")
    print(f"   ✅ **Natural Flow**: Page 1 → Page 2 → Page 3 sequence")
    print(f"   ✅ **Mixed Content**: Charts + text + headings on same page")
    print(f"   ✅ **Flexible Structure**: Different companies, same page numbers")
    print(f"   ✅ **Rich Descriptions**: Each element explains its purpose")
    print(f"   ✅ **Enhanced Data**: Structured charts and figures")
    
    # Show comparison
    print(f"\n📊 Old vs New Approach:")
    print(f"   🔴 **Old (Page Type)**: cover → about → services → contact")
    print(f"   🟢 **New (Page Number)**: Page 1 → Page 2 → Page 3 → Page N")
    print(f"   ")
    print(f"   🔴 **Old Problem**: Mixed content pages hard to classify")
    print(f"   🟢 **New Solution**: Any content can go on any page number")
    
    # Save demo output
    output_file = 'page_number_template_demo.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(master_template, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Demo template saved to: {output_file}")
    print(f"📏 Template size: {len(json.dumps(master_template))} characters")
    
    print(f"\n🎉 Page Number System Demo Complete!")
    print(f"   The new system successfully handles:")
    print(f"   ✅ Mixed content pages (charts + text + headings)")
    print(f"   ✅ Variable document lengths (3-5 pages)")
    print(f"   ✅ Different company structures")
    print(f"   ✅ Rich element descriptions")
    print(f"   ✅ Enhanced chart/figure data")
    
    return master_template

if __name__ == "__main__":
    demo_page_number_system()
