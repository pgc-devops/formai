import streamlit as st
import json
import xml.etree.ElementTree as ET
from test_form_vaildator import AdvancedComparisonAgent  # Assuming your backend code is saved as backend.py

def parse_form_input(input_data, form_type, agent):
    """Parse form input based on the selected format."""
    if not input_data.strip():
        return None
    
    try:
        if form_type == "JSON":
            return json.loads(input_data)
        elif form_type == "XML":
            return input_data.strip()
        elif form_type == "TEXT":
            return agent.extract_fields_from_text(input_data)
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in {form_type}! Please check your input.")
        return None
    except ET.ParseError:
        st.error(f"Invalid XML format in {form_type}! Please check your input.")
        return None
    return None

def main():
    st.set_page_config(page_title="Form Comparison Tool", layout="wide")
    st.title("📊 JSON, XML & TEXT Form Comparison Tool")
    
    agent = AdvancedComparisonAgent()
    
    # Form type selection
    form1_type = st.selectbox("Select format for Form 1:", ["JSON", "XML", "TEXT"], index=0, key="form1_type")
    form2_type = st.selectbox("Select format for Form 2:", ["JSON", "XML", "TEXT"], index=0, key="form2_type")
    
    # User inputs
    form1_input = st.text_area(f"Enter {form1_type} Form Data", height=200, key="form1_input")
    form2_input = st.text_area(f"Enter {form2_type} Form Data", height=200, key="form2_input")
    
    if st.button("Compare Forms ✨"):
        try:
            form1_data = parse_form_input(form1_input, form1_type, agent)
            form2_data = parse_form_input(form2_input, form2_type, agent)
            
            if not form1_data or not form2_data:
                st.warning("Please provide both form inputs for comparison.")
                return
            
            form1_fields = agent.extract_fields_from_json(form1_data) if form1_type == "JSON" else \
                           agent.extract_fields_from_xml(form1_data) if form1_type == "XML" else form1_data
            
            form2_fields = agent.extract_fields_from_json(form2_data) if form2_type == "JSON" else \
                           agent.extract_fields_from_xml(form2_data) if form2_type == "XML" else form2_data
            
            # Perform Comparison
            result = agent.compare_fields(form1_fields, form2_fields)
            
            # Display Results
            st.subheader("Comparison Results 📝")
            try:
                parsed_result = json.loads(result) if isinstance(result, str) else result
                st.json(parsed_result)
            except json.JSONDecodeError:
                st.markdown(result)  # Fallback to text display if JSON parsing fails
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
