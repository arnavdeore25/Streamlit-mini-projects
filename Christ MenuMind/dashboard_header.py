
import streamlit as st

def render_dashboard_header(selected_block, selected_outlet, food_preference, light_theme):
    # Live clock, date and greeting
    clock_html = """
        <div id="menumind-header" style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            padding: 16px 22px;
            margin: 4px 0 18px 0;
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 14px;
            background: __CLOCK_BG__;
            color: __CLOCK_TEXT__;
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        ">
            <div>
                <div id="greeting" style="font-size: 21px; font-weight: 700; margin-bottom: 5px;">
                    Welcome!
                </div>
                <div style="font-size: 13px; color: __CLOCK_MUTED__;">
                    Here's your campus food overview for today.
                </div>
            </div>
            <div style="text-align: right; min-width: 150px;">
                <div id="live-clock" style="font-size: 27px; font-weight: 700; letter-spacing: 1px;">
                    --:--:--
                </div>
                <div id="live-date" style="font-size: 13px; color: __CLOCK_MUTED__; margin-top: 3px;">
                    Loading date...
                </div>
            </div>
        </div>

        <script>
            function updateMenuMindHeader() {
                const now = new Date();
                const hour = now.getHours();

                let greeting = "Good evening";
                if (hour >= 5 && hour < 12) {
                    greeting = "Good morning";
                } else if (hour >= 12 && hour < 17) {
                    greeting = "Good afternoon";
                }

                document.getElementById("greeting").textContent = greeting + "!";
                document.getElementById("live-clock").textContent =
                    now.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit"
                    });
                document.getElementById("live-date").textContent =
                    now.toLocaleDateString([], {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                        year: "numeric"
                    });
            }

            updateMenuMindHeader();
            setInterval(updateMenuMindHeader, 1000);
        </script>
        """

    clock_html = (
        clock_html
        .replace("__CLOCK_BG__", "linear-gradient(110deg, #FFFFFF, #EAF1F7)" if light_theme else "linear-gradient(110deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.88))")
        .replace("__CLOCK_TEXT__", "#263445" if light_theme else "#F8FAFC")
        .replace("__CLOCK_MUTED__", "#64748B" if light_theme else "#CBD5E1")
    )
    st.components.v1.html(clock_html, height=112, scrolling=False)



    # Main dashboard
    st.title("🍽️ Christ MenuMind")
    st.subheader("Eat Smart. Explore Better. Decide with Data.")

    st.write(
        "An intelligent campus food analytics platform "
        "for exploring food menus, prices, sales and student preferences."
    )

    # Active filter summary
    active_block_label = selected_block
    active_outlet_label = selected_outlet
    active_food_label = {
        "All": "All Food Types",
        "Veg": "Vegetarian",
        "Non-Veg": "Non-Vegetarian (Chicken)"
    }[food_preference]

    st.markdown("### 🔎 Active Filters")
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        st.markdown(
            f"""
            <div style="
                padding: 12px 16px;
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 10px;
                background: rgba(30, 41, 59, 0.45);
            ">
                <div style="font-size: 12px; color: #94A3B8;">CAMPUS BLOCK</div>
                <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                    {active_block_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with filter_col2:
        st.markdown(
            f"""
            <div style="
                padding: 12px 16px;
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 10px;
                background: rgba(30, 41, 59, 0.45);
            ">
                <div style="font-size: 12px; color: #94A3B8;">OUTLET</div>
                <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                    {active_outlet_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with filter_col3:
        st.markdown(
            f"""
            <div style="
                padding: 12px 16px;
                border: 1px solid rgba(148, 163, 184, 0.25);
                border-radius: 10px;
                background: rgba(30, 41, 59, 0.45);
            ">
                <div style="font-size: 12px; color: #94A3B8;">FOOD PREFERENCE</div>
                <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">
                    {active_food_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True  
        )

    st.divider()

