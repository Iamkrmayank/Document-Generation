import streamlit as st
import json
import traceback
from typing import List, Dict, Any
import os

from bedrock_client import BedrockClient
from parsing import DocumentParser
from template_inference import TemplateInferenceEngine

def main():
    st.set_page_config(
        page_title="Master Template Generator",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Master Template Generator")
    st.markdown("Upload company profile documents to generate a master template structure")
    
    # Initialize session state
    if 'generated_template' not in st.session_state:
        st.session_state.generated_template = None
    if 'processing_logs' not in st.session_state:
        st.session_state.processing_logs = []
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # AWS Region (optional override)
        aws_region = st.selectbox(
            "AWS Region",
            ["eu-west-1", "us-east-1", "us-west-2"],
            index=0
        )
        
        # Model configuration
        st.info("Using Claude Sonnet 4.5 on AWS Bedrock")
        
        # Clear results button
        if st.button("Clear Results"):
            st.session_state.generated_template = None
            st.session_state.processing_logs = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Upload 2-3 company profile documents (PDF or PPTX)",
            type=["pdf", "pptx"],
            accept_multiple_files=True,
            help="Upload sample company profile documents to analyze their structure"
        )
        
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size:,} bytes)")
        
        # Generate template button
        generate_button = st.button(
            "🚀 Generate Master Template",
            disabled=len(uploaded_files) < 2 if uploaded_files else True,
            help="Upload at least 2 documents to generate a template"
        )
    
    with col2:
        st.header("Processing Status")
        
        # Processing logs container
        log_container = st.container()
        
        if generate_button and uploaded_files:
            process_documents(uploaded_files, aws_region, log_container)
    
    # Results section
    if st.session_state.generated_template:
        st.header("Generated Master Template")
        
        template = st.session_state.generated_template
        
        # Comprehensive template summary with catalog integration
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Pages", len(template.get('pages', [])))
        with col2:
            total_blocks = sum(len(page.get('blocks', [])) for page in template.get('pages', []))
            st.metric("Total Blocks", total_blocks)
        with col3:
            st.metric("Document Fields", len(template.get('document_fields', [])))
        with col4:
            st.metric("Common Elements", len(template.get('common_elements', [])))
        with col5:
            catalog_integration = template.get('catalog_integration', {})
            coverage = catalog_integration.get('coverage_analysis', {}).get('coverage_percentage', 0)
            st.metric("Catalog Coverage", f"{coverage}%")
        
        # Catalog Integration Summary
        if 'catalog_integration' in template:
            st.subheader("📋 Master Catalog Integration")
            catalog_info = template['catalog_integration']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Catalog Information:**")
                st.write(f"• **Catalog ID:** {catalog_info.get('catalog_id', 'Unknown')}")
                st.write(f"• **Version:** {catalog_info.get('catalog_version', 'Unknown')}")
                st.write(f"• **Name:** {catalog_info.get('catalog_name', 'Unknown')}")
            
            with col2:
                st.write("**Element Mapping:**")
                coverage = catalog_info.get('coverage_analysis', {})
                st.write(f"• **Total Detected:** {coverage.get('total_elements_detected', 0)}")
                st.write(f"• **Mapped to Catalog:** {coverage.get('elements_mapped_to_catalog', 0)}")
                st.write(f"• **Coverage:** {coverage.get('coverage_percentage', 0)}%")
            
            with col3:
                st.write("**Unmapped Elements:**")
                unmapped = coverage.get('unmapped_elements', [])
                if unmapped:
                    for element in unmapped[:5]:
                        st.write(f"• {element}")
                    if len(unmapped) > 5:
                        st.write(f"• ... and {len(unmapped) - 5} more")
                else:
                    st.write("• All elements mapped! ✅")
        
        # Analysis Summary
        if 'analysis_summary' in template:
            st.subheader("📊 Document Analysis Summary")
            analysis = template['analysis_summary']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Document Structure Analysis:**")
                for doc_id, structure in analysis['document_structure'].items():
                    with st.expander(f"📄 {doc_id.upper()} ({structure['total_pages']} pages)"):
                        st.write(f"**Page Roles:** {', '.join(set(structure['page_roles']))}")
                        st.write(f"**Element Categories:** {', '.join(structure['element_categories'])}")
                        st.write(f"**Has Front Matter:** {'✅' if structure['has_front_matter'] else '❌'}")
                        st.write(f"**Has Analysis:** {'✅' if structure['has_analysis'] else '❌'}")
                        st.write(f"**Has Recommendations:** {'✅' if structure['has_recommendations'] else '❌'}")
                        st.write(f"**Has End Matter:** {'✅' if structure['has_end_matter'] else '❌'}")
            
            with col2:
                st.write("**Common Elements Across Documents:**")
                # Show catalog-based elements if available
                catalog_elements = template.get('catalog_based_elements', [])
                if catalog_elements:
                    st.write("**(From Master Catalog):**")
                    for element in catalog_elements[:8]:
                        percentage = element.get('frequency_percentage', 0)
                        mapping_status = "✅" if element.get('mapping_status') == 'mapped' else "⚠️"
                        st.write(f"• {mapping_status} **{element['element_type']}** ({element['category']}): {percentage:.1f}%")
                
                # Show regular common elements
                for element in template.get('common_elements', [])[:5]:
                    percentage = element.get('percentage', 0)
                    st.write(f"• **{element['element_type']}** ({element['element_category']}): {percentage:.1f}%")
        
        # Element Frequency Analysis
        if 'element_frequency' in template:
            st.subheader("📈 Element Frequency Analysis")
            
            # Create frequency chart data
            freq_data = []
            for element_type, stats in template['element_frequency'].items():
                freq_data.append({
                    'Element': element_type,
                    'Document %': stats['document_percentage'],
                    'Total Count': stats['total_count']
                })
            
            # Sort by frequency
            freq_data = sorted(freq_data, key=lambda x: x['Document %'], reverse=True)[:15]
            
            # Display as table
            st.write("**Top 15 Most Common Elements:**")
            for i, item in enumerate(freq_data, 1):
                st.write(f"{i}. **{item['Element']}**: {item['Document %']:.1f}% ({item['Total Count']} occurrences)")
        
        # Page Structure Analysis
        st.subheader("📑 Template Page Structure")
        
        for page in template['pages']:
            required_status = "🔴 Required" if page['required'] else "🟡 Optional"
            frequency = page.get('frequency_percentage', 0)
            
            # Handle both old and new page structure
            page_number = page.get('page_number', page.get('page_index', 1))
            page_title = page.get('page_title', page.get('title', f'Page {page_number}'))
            page_role = page.get('page_role', page.get('page_type', 'unknown'))
            content_types = page.get('content_types', [])
            
            # Create content type icons
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
            
            with st.expander(f"📄 **PAGE {page_number}** - {page_title} - {required_status} ({frequency}%) {content_display}"):
                st.write(f"**Page Number:** {page_number}")
                st.write(f"**Page Role:** {page_role}")
                if content_types:
                    st.write(f"**Content Types:** {', '.join(content_types)}")
                st.write(f"**Document Count:** {page.get('document_count', 0)}")
                st.write(f"**Total Blocks:** {len(page.get('blocks', []))}")
                
                # Block details
                st.write("**Blocks:**")
                for block in page['blocks']:
                    mode_icon = "🔄" if block['content_mode'] == 'dynamic' else "📌"
                    optional_icon = "🟡" if block['optional'] else "🔴"
                    catalog_icon = "📋" if block.get('catalog_mapped', False) else "⚠️"
                    importance = block.get('importance', 'unknown')
                    category = block.get('category', 'unknown')
                    
                    st.write(f"  {mode_icon} {optional_icon} {catalog_icon} **{block['type']}** ({category}, {importance})")
                    
                    # Show element description
                    if block.get('description'):
                        st.write(f"    💡 **Description:** {block['description']}")
                    
                    # Show mapping status
                    mapping_status = block.get('mapping_status', 'unknown')
                    if mapping_status == 'mapped':
                        st.write(f"    ✅ Mapped to catalog")
                    elif mapping_status == 'unmapped':
                        st.write(f"    ⚠️ Custom element (not in catalog)")
                    
                    # Show chart data if available
                    if block.get('chart_data'):
                        chart = block['chart_data']
                        st.write(f"    📊 **Chart:** {chart.get('title', 'Untitled')} ({chart.get('chart_type', 'unknown')})")
                        if chart.get('description'):
                            st.write(f"        📝 {chart['description']}")
                        if chart.get('data'):
                            st.write(f"        📈 Data points: {len(chart['data'])}")
                            # Show first few data points
                            for i, data_point in enumerate(chart['data'][:3]):
                                name = data_point.get('name', f'Item {i+1}')
                                value = data_point.get('value', 'N/A')
                                unit = data_point.get('unit', '')
                                st.write(f"          • {name}: {value} {unit}")
                            if len(chart['data']) > 3:
                                st.write(f"          • ... and {len(chart['data']) - 3} more")
                    
                    # Show figure data if available
                    if block.get('figure_data'):
                        figure = block['figure_data']
                        st.write(f"    🖼️ **Figure:** {figure.get('title', 'Untitled')} ({figure.get('figure_type', 'unknown')})")
                        if figure.get('description'):
                            st.write(f"        📝 {figure['description']}")
                        if figure.get('elements'):
                            st.write(f"        🔍 Elements: {len(figure['elements'])}")
                            # Show first few elements
                            for i, element in enumerate(figure['elements'][:3]):
                                name = element.get('name', f'Element {i+1}')
                                value = element.get('value', 'N/A')
                                st.write(f"          • {name}: {value}")
                            if len(figure['elements']) > 3:
                                st.write(f"          • ... and {len(figure['elements']) - 3} more")
                    
                    if block['content_mode'] == 'static' and block.get('static_text'):
                        st.write(f"    📝 Static: \"{block['static_text'][:100]}...\"")
                    elif block['content_mode'] == 'dynamic' and block.get('field_schema'):
                        field = block['field_schema']
                        pii_info = f" [{field['pii_type']}]" if field['pii_type'] != 'NONE' else ""
                        st.write(f"    🔄 Dynamic: {field['field_id']} ({field['data_type']}){pii_info}")
        
        # Global Fields
        st.subheader("🌐 Global Document Fields")
        for field in template['document_fields']:
            pii_info = f" [{field['pii_type']}]" if field['pii_type'] != 'NONE' else ""
            importance = field.get('importance', 'unknown')
            category = field.get('category', 'unknown')
            st.write(f"• **{field['field_id']}**: {field['label']} ({field['data_type']}, {importance}, {category}){pii_info}")
        
        # Full Template JSON (collapsible)
        with st.expander("🔍 View Complete Template JSON"):
            st.json(template)
        
        # Download button
        template_json = json.dumps(template, indent=2)
        st.download_button(
            label="📥 Download Comprehensive Template JSON",
            data=template_json,
            file_name="comprehensive_master_template.json",
            mime="application/json",
            help="Download the comprehensive template with full analysis"
        )

def process_documents(uploaded_files: List, aws_region: str, log_container):
    """Process uploaded documents and generate master template"""
    
    try:
        # Initialize components
        bedrock_client = BedrockClient(region=aws_region)
        parser = DocumentParser()
        inference_engine = TemplateInferenceEngine(bedrock_client)
        
        with log_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Parse documents
            status_text.text("📖 Parsing documents...")
            all_page_data = []
            
            for i, file in enumerate(uploaded_files):
                try:
                    status_text.text(f"📖 Parsing {file.name}...")
                    
                    # Parse document
                    pages = parser.parse_document(file)
                    
                    # Extract structured data for each page
                    for page_idx, page_content in enumerate(pages):
                        status_text.text(f"🔍 Analyzing {file.name} - Page {page_idx + 1}")
                        
                        page_json = bedrock_client.extract_page_structure(
                            page_content, 
                            doc_id=f"doc_{i+1}", 
                            page_index=page_idx + 1
                        )
                        
                        if page_json:
                            all_page_data.append(page_json)
                    
                    progress_bar.progress((i + 1) / len(uploaded_files) * 0.7)
                    
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
                    continue
            
            # Step 2: Generate master template
            if all_page_data:
                status_text.text("🧠 Generating master template...")
                progress_bar.progress(0.8)
                
                master_template = inference_engine.infer_master_template(all_page_data)
                
                progress_bar.progress(1.0)
                status_text.text("✅ Template generation complete!")
                
                # Store in session state
                st.session_state.generated_template = master_template
                
                st.success(f"Successfully processed {len(uploaded_files)} documents with {len(all_page_data)} pages total")
                
            else:
                st.error("No page data could be extracted from the uploaded documents")
                
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        st.error("Full error details:")
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
