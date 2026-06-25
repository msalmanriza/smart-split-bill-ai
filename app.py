import streamlit as st
import matplotlib.pyplot as plt
from services.gemini_reader import extract_receipt
from utils.split_calculator import calculate_split

st.set_page_config(
    page_title="Smart Split Bill AI",
    page_icon="🧾",
    layout="wide"
)

with st.sidebar:

    st.title("🧾 Smart Split Bill AI")
    st.success("Gemini 2.5 Flash")

    st.divider()

    st.subheader("Workflow")

    st.markdown("""
    1. Upload Receipt
    2. Extract Receipt
    3. Add Participants
    4. Assign Items
    5. Calculate Split
    6. View Result
    """)

    st.divider()

    if st.button(
        "🗑️ Clear Session",
        use_container_width=True
    ):
        st.session_state.clear()
        st.rerun()

st.title("🧾 Smart Split Bill AI")

st.caption(
    "AI-powered receipt extraction and bill splitting"
)

uploaded_files = st.file_uploader(
    "Upload receipt",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:

    if "receipt_extracted" not in st.session_state:
        st.session_state.receipt_extracted = False

    if st.button(
        "🔍 Extract Receipt",
        use_container_width=True
    ):
        st.session_state.receipt_extracted = True

    if not st.session_state.receipt_extracted:
        st.stop()

    all_items = []
    grand_total = 0

    st.subheader("📷 Receipt Preview")

    preview_cols = st.columns(
        min(len(uploaded_files), 3)
    )

    for i, uploaded_file in enumerate(uploaded_files):

        with open(
            uploaded_file.name,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        cache_key = f"receipt_{uploaded_file.name}"

        if cache_key not in st.session_state:
            st.session_state[cache_key] = (
                extract_receipt(
                    uploaded_file.name
                )
            )

        receipt = st.session_state[
            cache_key
        ]

        st.session_state["receipt"] = receipt
        receipt = st.session_state["receipt"]

        if "items" not in receipt:
            continue

        all_items.extend(
            receipt["items"]
        )

        grand_total += receipt.get(
            "total_bill",
            0
        )

        with preview_cols[
            i % len(preview_cols)
        ]:

            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_container_width=True,
                width=150
            )

    if not all_items:

        st.error(
            "Failed to extract receipt data."
        )

        st.stop()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "📊 Extracted Data"
        )

        st.dataframe(
            all_items,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "Summary"
        )

        st.metric(
            "Items",
            len(all_items)
        )

        st.metric(
            "Total Bill",
            f"Rp {grand_total:,.0f}"
        )

    st.divider()

    st.subheader(
        "👥 Participants"
    )

    if "participant_count" not in st.session_state:
        st.session_state.participant_count = 1

    col1, col2 = st.columns(2)

    with col1:
        if st.button(" Add Participant"):

            st.session_state.participant_count += 1

    with col2:
        if (
            st.button(" Remove Participant")
            and st.session_state.participant_count > 1
        ):
            st.session_state.participant_count -= 1

    people = []

    for i in range(
        st.session_state.participant_count
    ):
        
        name = st.text_input(
            f"participant {i+1}",
            key=f"participant_{i}"
        )

        if name.strip():
            people.append(
                name.strip()
            )

    if len(people) > 0:

        st.subheader(
            "🛒 Assign Items"
        )

        for index, item in enumerate(
            all_items
        ):

            payer = st.selectbox(
                f"{item['name']} - Rp {item['total_price']:,.0f}",
                people,
                key=f"item_{index}"
            )

            item["payer"] = payer

        assigned_data = []

        for item in all_items:

            assigned_data.append(
                {
                    "Item": item["name"],
                    "Price": f"Rp {item['total_price']:,.0f}",
                    "Payer": item.get(
                        "payer",
                        "-"
                    )
                }
            )

        st.subheader(
            "📋 Calculate Split"
        )

        st.dataframe(
            assigned_data,
            use_container_width=True
        )

        calculate = st.button(
            "💰 Calculate Split",
            use_container_width=True
        )

        if calculate:

            summary = calculate_split(
                all_items
            )

            st.subheader(
                "💰 Split Result"
            )

            cols = st.columns(
                len(summary)
            )

            for col, (person, total) in zip(
                cols,
                summary.items()
            ):
                
                with col:
                    st.metric(
                        person,
                        f"Rp {total:,.0f}"
                    )

            st.subheader(
                " Split Visualization"
            )

            fig, ax = plt.subplots(
                figsize=(5, 5)
            )

            ax.pie(
                list(summary.values()),
                labels=list(summary.keys()),
                autopct="%1.1f%%"
            )

            ax.axis("equal")

            st.pyplot(fig)

            split_total = sum(
                summary.values()
            )

            bill_total = grand_total

            st.subheader(
                "📄 Final Report"
            )

            report_data = []

            for person, total in summary.items():

                report_data.append(
                    {
                        "Participant": person,
                        "Amount": f"Rp {total:,.0f}"
                    }
                )

            st.dataframe(
                report_data,
                use_container_width=True
            )

            split_total = sum(
                summary.values()
            )

            bill_total = grand_total

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Bill Total",
                    f"Rp {bill_total:,.0f}"
                )

            with col2:

                st.metric(
                    "Split Total",
                    f"Rp {split_total:,.0f}"
                )

            st.subheader(
                "📌 Summary"
            )

            st.write(
                f"Total Participants: {len(summary)}"
            )

            st.write(
                f"Total Items: {len(all_items)}"
            )

            st.write(
                f"Total Receipt: Rp {bill_total:,.0f}"
            )

            st.subheader(
                "✅ Validation"
            )

            difference = (
                bill_total
                - split_total
            )

            if difference == 0:

                st.success(
                    "Total matched"
                )

            else:

                st.warning(
                    f"Difference: Rp {difference:,.0f}"
                )

                st.info(
                    "Additional charges or OCR extraction may not be fully captured."
                )