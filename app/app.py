from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon=None,
    layout="wide"
)


APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
RESULTS_DIR = PROJECT_DIR / "results"


def read_csv_safe(file_name):
    file_path = RESULTS_DIR / file_name

    if not file_path.exists():
        return None

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.warning(f"Không đọc được file {file_name}: {error}")
        return None


@st.cache_data
def load_data():
    data = {
        "rules": read_csv_safe("association_rules_filtered.csv"),
        "recommendations": read_csv_safe("recommendation_lookup.csv"),
        "rules_summary": read_csv_safe("association_rules_summary.csv"),
        "frequent_summary": read_csv_safe("experiment_frequent_itemsets_summary.csv"),
        "deep_summary": read_csv_safe("deep_analysis_summary.csv"),
        "core_departments": read_csv_safe("department_core_analysis.csv"),
        "layout_pairs": read_csv_safe("department_layout_recommendation.csv"),
        "promotion_candidates": read_csv_safe("promotion_bundle_candidates.csv"),
        "department_roles": read_csv_safe("department_role_classification.csv"),
        "reordered_analysis": read_csv_safe("recommended_products_reordered_analysis.csv"),
        "top_antecedent_products": read_csv_safe("top_antecedent_products.csv"),
        "top_recommended_products": read_csv_safe("top_recommended_products.csv"),
        "department_pairs": read_csv_safe("department_pair_analysis.csv"),
        "department_scope": read_csv_safe("department_scope_summary.csv"),
    }

    return data


def format_percent(series):
    return (series * 100).round(2)


def show_metric_cards(data):
    rules = data["rules"]
    recommendations = data["recommendations"]
    core_departments = data["core_departments"]
    promotion_candidates = data["promotion_candidates"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        value = len(rules) if rules is not None else 0
        st.metric("Luật sau lọc", value)

    with col2:
        value = len(recommendations) if recommendations is not None else 0
        st.metric("Luật dùng cho gợi ý", value)

    with col3:
        value = len(core_departments) if core_departments is not None else 0
        st.metric("Ngành hàng phân tích", value)

    with col4:
        value = len(promotion_candidates) if promotion_candidates is not None else 0
        st.metric("Luật đề xuất combo", value)


def page_overview(data):
    st.title("Market Basket Analysis - Association Rule Mining")

    st.write(
        """
        Ứng dụng này trình bày kết quả khai thác luật kết hợp trên dữ liệu giỏ hàng siêu thị.
        Các thuật toán khai thác luật đã được chạy offline bằng Python. Web demo chỉ đọc các file kết quả
        trong thư mục `results` để tra cứu luật, gợi ý sản phẩm và trình bày insight kinh doanh.
        """
    )

    show_metric_cards(data)

    st.subheader("Pipeline xử lý")
    st.write(
        """
        Dữ liệu giao dịch đã xử lý  
        → Ma trận giao dịch - sản phẩm  
        → FP-Growth / Apriori  
        → Frequent Itemsets  
        → Association Rules  
        → Rule Filtering  
        → Recommendation Lookup  
        → Web Demo
        """
    )

    if data["frequent_summary"] is not None:
        st.subheader("So sánh thực nghiệm FP-Growth và Apriori")
        st.dataframe(data["frequent_summary"], use_container_width=True)

    if data["rules_summary"] is not None:
        st.subheader("Tóm tắt luật kết hợp")
        st.dataframe(data["rules_summary"], use_container_width=True)

    if data["deep_summary"] is not None:
        st.subheader("Tóm tắt phân tích mở rộng")
        st.dataframe(data["deep_summary"], use_container_width=True)


def page_rule_lookup(data):
    st.title("Tra cứu luật kết hợp")

    rules = data["rules"]

    if rules is None or rules.empty:
        st.warning("Không tìm thấy association_rules_filtered.csv.")
        return

    st.write(
        """
        Trang này cho phép tra cứu các luật kết hợp đã được lọc bằng support, confidence, lift
        và độ dài luật. Đây là bảng luật chính dùng cho phân tích.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        min_support = st.number_input(
            "Min support",
            min_value=0.0,
            max_value=1.0,
            value=float(rules["support"].min()),
            step=0.001,
            format="%.4f"
        )

    with col2:
        min_confidence = st.number_input(
            "Min confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.20,
            step=0.01,
            format="%.2f"
        )

    with col3:
        min_lift = st.number_input(
            "Min lift",
            min_value=0.0,
            value=1.20,
            step=0.10,
            format="%.2f"
        )

    with col4:
        top_n = st.number_input(
            "Số dòng hiển thị",
            min_value=5,
            max_value=200,
            value=30,
            step=5
        )

    keyword = st.text_input("Tìm theo tên sản phẩm", "")

    filtered = rules[
        (rules["support"] >= min_support) &
        (rules["confidence"] >= min_confidence) &
        (rules["lift"] >= min_lift)
    ].copy()

    if keyword.strip():
        keyword_lower = keyword.lower()
        filtered = filtered[
            filtered["antecedent_names"].str.lower().str.contains(keyword_lower, na=False) |
            filtered["consequent_names"].str.lower().str.contains(keyword_lower, na=False)
        ]

    sort_options = [
        col for col in [
            "weighted_recommendation_score",
            "recommendation_score",
            "confidence",
            "lift",
            "support",
            "support_count"
        ]
        if col in filtered.columns
    ]

    sort_col = st.selectbox("Sắp xếp theo", sort_options)

    filtered = filtered.sort_values(sort_col, ascending=False)

    display_cols = [
        "antecedent_names",
        "consequent_names",
        "support",
        "support_count",
        "confidence",
        "lift",
        "recommendation_score",
        "weighted_recommendation_score",
        "antecedent_departments",
        "consequent_departments",
        "antecedent_aisles",
        "consequent_aisles"
    ]

    display_cols = [col for col in display_cols if col in filtered.columns]

    st.write(f"Số luật phù hợp: {len(filtered)}")
    st.dataframe(filtered[display_cols].head(int(top_n)), use_container_width=True)


def page_recommendation(data):
    st.title("Gợi ý sản phẩm mua kèm")

    recommendations = data["recommendations"]
    rules = data["rules"]

    st.write(
        """
        Người dùng chọn hoặc nhập một sản phẩm đầu vào, hệ thống sẽ tìm các luật có sản phẩm đó
        ở vế trái và trả về các sản phẩm nên mua kèm ở vế phải.
        """
    )

    recommendation_mode = st.radio(
        "Chọn chế độ gợi ý",
        [
            "Gợi ý đơn sản phẩm (1 sản phẩm → 1 sản phẩm)",
            "Gợi ý mở rộng từ toàn bộ luật"
        ],
        horizontal=True
    )

    if recommendation_mode == "Gợi ý đơn sản phẩm (1 sản phẩm → 1 sản phẩm)":
        if recommendations is None or recommendations.empty:
            st.warning("Không tìm thấy recommendation_lookup.csv.")
            return

        st.info(
            "Chế độ này chỉ dùng các luật đơn giản dạng 1 sản phẩm đầu vào → 1 sản phẩm gợi ý. "
            "Phù hợp để demo recommendation rõ ràng và dễ giải thích."
        )

        product_list = sorted(recommendations["input_product_name"].dropna().unique())
        selected_product = st.selectbox("Chọn sản phẩm đầu vào", product_list)

        sort_options = [
            col for col in [
                "weighted_recommendation_score",
                "recommendation_score",
                "confidence",
                "lift",
                "support_count",
                "support"
            ]
            if col in recommendations.columns
        ]

        col1, col2 = st.columns(2)

        with col1:
            sort_col = st.selectbox("Sắp xếp gợi ý theo", sort_options)

        with col2:
            top_n = st.slider("Số sản phẩm gợi ý", min_value=3, max_value=20, value=10)

        result = recommendations[
            recommendations["input_product_name"] == selected_product
        ].copy()

        result = result.sort_values(sort_col, ascending=False).head(top_n)

        display_cols = [
            "recommended_product_name",
            "support",
            "support_count",
            "confidence",
            "lift",
            "recommendation_score",
            "weighted_recommendation_score",
            "consequent_departments",
            "consequent_aisles"
        ]

        display_cols = [col for col in display_cols if col in result.columns]

        st.subheader(f"Sản phẩm gợi ý cho: {selected_product}")

        if result.empty:
            st.info("Sản phẩm này chưa có luật gợi ý phù hợp ở chế độ đơn sản phẩm.")
            return

        st.dataframe(result[display_cols], use_container_width=True)

        fig = px.bar(
            result,
            x="recommended_product_name",
            y=sort_col,
            title=f"Top sản phẩm gợi ý theo {sort_col}",
            labels={
                "recommended_product_name": "Sản phẩm gợi ý",
                sort_col: "Điểm xếp hạng"
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    else:
        if rules is None or rules.empty:
            st.warning("Không tìm thấy association_rules_filtered.csv.")
            return

        st.info(
            "Chế độ mở rộng dùng toàn bộ luật đã lọc. Chỉ cần sản phẩm xuất hiện trong vế trái "
            "của luật, hệ thống sẽ trả về vế phải làm gợi ý. Với luật có nhiều sản phẩm ở vế trái, "
            "gợi ý mạnh nhất khi người dùng có đủ các sản phẩm trong điều kiện luật."
        )

        keyword = st.text_input(
            "Nhập tên sản phẩm đầu vào",
            value="",
            placeholder="Ví dụ: banana, yogurt, milk..."
        )

        sort_options = [
            col for col in [
                "weighted_recommendation_score",
                "recommendation_score",
                "confidence",
                "lift",
                "support_count",
                "support"
            ]
            if col in rules.columns
        ]

        col1, col2 = st.columns(2)

        with col1:
            sort_col = st.selectbox("Sắp xếp gợi ý theo", sort_options, key="expanded_sort_col")

        with col2:
            top_n = st.slider("Số luật gợi ý hiển thị", min_value=3, max_value=50, value=10)

        if not keyword.strip():
            st.info("Nhập tên sản phẩm để tìm gợi ý mở rộng từ toàn bộ luật.")
            return

        keyword_lower = keyword.strip().lower()
        result = rules[
            rules["antecedent_names"].str.lower().str.contains(keyword_lower, na=False, regex=False)
        ].copy()

        if result.empty:
            st.warning(
                "Không tìm thấy luật có sản phẩm này ở vế trái. "
                "Anh có thể thử từ khóa ngắn hơn, ví dụ: banana, yogurt, milk."
            )
            return

        result = result.sort_values(sort_col, ascending=False).head(top_n)

        display_cols = [
            "antecedent_names",
            "consequent_names",
            "support",
            "support_count",
            "confidence",
            "lift",
            "recommendation_score",
            "weighted_recommendation_score",
            "antecedent_departments",
            "consequent_departments",
            "antecedent_aisles",
            "consequent_aisles"
        ]

        display_cols = [col for col in display_cols if col in result.columns]

        st.subheader(f"Luật gợi ý mở rộng cho từ khóa: {keyword.strip()}")
        st.write(f"Số luật tìm được: {len(rules[rules['antecedent_names'].str.lower().str.contains(keyword_lower, na=False, regex=False)])}")
        st.dataframe(result[display_cols], use_container_width=True)

        chart_data = result.copy()
        chart_data["rule_label"] = chart_data["antecedent_names"].astype(str) + " → " + chart_data["consequent_names"].astype(str)

        fig = px.bar(
            chart_data,
            x="rule_label",
            y=sort_col,
            title=f"Top luật gợi ý mở rộng theo {sort_col}",
            labels={
                "rule_label": "Luật gợi ý",
                sort_col: "Điểm xếp hạng"
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def page_business_insights(data):
    st.title("Phân tích ứng dụng cho siêu thị")

    st.write(
        """
        Trang này trình bày các phân tích mở rộng từ luật kết hợp, nhằm hỗ trợ các quyết định thực tế
        như xác định ngành hàng trung tâm, bố trí quầy hàng, thiết kế combo và chiến lược bán chéo.
        """
    )

    core_departments = data["core_departments"]
    layout_pairs = data["layout_pairs"]
    promotion_candidates = data["promotion_candidates"]
    department_roles = data["department_roles"]
    reordered_analysis = data["reordered_analysis"]

    if core_departments is not None:
        st.subheader("Ngành hàng trung tâm")
        st.dataframe(core_departments.head(15), use_container_width=True)

        if "core_score" in core_departments.columns:
            fig = px.bar(
                core_departments.head(10),
                x="department",
                y="core_score",
                title="Top ngành hàng trung tâm theo core_score",
                labels={
                    "department": "Ngành hàng",
                    "core_score": "Core score"
                }
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    if layout_pairs is not None:
        st.subheader("Cặp ngành hàng nên cân nhắc đặt gần nhau")
        st.dataframe(layout_pairs.head(15), use_container_width=True)

        if "layout_priority_score" in layout_pairs.columns:
            fig = px.bar(
                layout_pairs.head(10),
                x="department_pair",
                y="layout_priority_score",
                title="Top cặp ngành hàng theo layout priority score",
                labels={
                    "department_pair": "Cặp ngành hàng",
                    "layout_priority_score": "Điểm ưu tiên bố trí"
                }
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    if promotion_candidates is not None:
        st.subheader("Luật phù hợp để tạo combo hoặc khuyến mãi")

        display_cols = [
            "antecedent_names",
            "consequent_names",
            "promotion_type",
            "support_count",
            "confidence",
            "lift",
            "weighted_recommendation_score",
            "antecedent_departments",
            "consequent_departments"
        ]

        display_cols = [col for col in display_cols if col in promotion_candidates.columns]

        st.dataframe(promotion_candidates[display_cols].head(20), use_container_width=True)

    if department_roles is not None:
        st.subheader("Vai trò của ngành hàng trong hệ thống gợi ý")
        st.dataframe(department_roles.head(20), use_container_width=True)

    if reordered_analysis is not None:
        st.subheader("Sản phẩm được gợi ý và hành vi mua lại")
        st.dataframe(reordered_analysis.head(20), use_container_width=True)


def page_dashboard(data):
    st.title("Dashboard tổng quan")

    rules = data["rules"]
    department_scope = data["department_scope"]
    top_antecedent = data["top_antecedent_products"]
    top_recommended = data["top_recommended_products"]
    department_pairs = data["department_pairs"]

    if rules is not None:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                rules,
                x="confidence",
                nbins=30,
                title="Phân bố confidence của các luật"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.histogram(
                rules,
                x="lift",
                nbins=30,
                title="Phân bố lift của các luật"
            )
            st.plotly_chart(fig, use_container_width=True)

    if department_scope is not None:
        st.subheader("Same department và Cross department")
        st.dataframe(department_scope, use_container_width=True)

        if "num_rules" in department_scope.columns:
            fig = px.pie(
                department_scope,
                names="department_scope",
                values="num_rules",
                title="Tỷ lệ luật cùng ngành hàng và khác ngành hàng"
            )
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if top_antecedent is not None:
            st.subheader("Top sản phẩm kích hoạt gợi ý")
            st.dataframe(top_antecedent.head(10), use_container_width=True)

    with col2:
        if top_recommended is not None:
            st.subheader("Top sản phẩm thường được gợi ý")
            st.dataframe(top_recommended.head(10), use_container_width=True)

    if department_pairs is not None:
        st.subheader("Top cặp department trong luật kết hợp")
        st.dataframe(department_pairs.head(15), use_container_width=True)


data = load_data()

st.sidebar.title("Điều hướng")

page = st.sidebar.radio(
    "Chọn trang",
    [
        "Tổng quan",
        "Tra cứu luật kết hợp",
        "Gợi ý sản phẩm",
        "Phân tích ứng dụng",
        "Dashboard"
    ]
)

if page == "Tổng quan":
    page_overview(data)
elif page == "Tra cứu luật kết hợp":
    page_rule_lookup(data)
elif page == "Gợi ý sản phẩm":
    page_recommendation(data)
elif page == "Phân tích ứng dụng":
    page_business_insights(data)
elif page == "Dashboard":
    page_dashboard(data)