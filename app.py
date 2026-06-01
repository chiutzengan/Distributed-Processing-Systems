import streamlit as st
import requests
st.set_page_config(page_title="分散式系統 - Open Data 串接")
st.title("🚲 台北市 YouBike 2.0 即時車位查詢 (REST API)")
st.write("這是一個分散式系統的 Client 端，點擊按鈕將會透過 HTTP 請求，向台北市政府的遠端伺服器獲取最新的 JSON 狀態。")
all_districts = ["大安區", "信義區", "文山區", "中山區", "中正區", "大同區", "松山區", "萬華區", "士林區", "北投區", "內湖區", "南港區", "臺大公館校區"]
district = st.selectbox("請選擇要查詢的行政區：", all_districts)
display_count = st.slider("請選擇要顯示的站點數量：", min_value=1, max_value=50, value=5)
if st.button("查詢即時資料"):
    with st.spinner("透過 REST API 向台北市政府請求資料中..."):
        url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"        
        try:
            response = requests.get(url)            
            if response.status_code == 200:
                data = response.json()                
                filtered_data = [station for station in data if station.get('sarea') == district]                
                st.success(f"🎉 成功從遠端伺服器取得 JSON 資料！該區共有 {len(filtered_data)} 個站點。")
                st.markdown(f"### ⬇️ 以下為即時解析的結果 (顯示前 {display_count} 筆)：")
                for station in filtered_data[:display_count]:
                    station_name = station.get('sna', '未知站點').replace('YouBike2.0_', '')
                    rent_bikes = station.get('available_rent_bikes', station.get('sbi', '未知'))
                    return_bikes = station.get('available_return_bikes', station.get('bemp', '未知'))                    
                    st.info(f"📍 **{station_name}**\n* 🚲 可借車輛：**{rent_bikes}** 輛\n* 🅿️ 空車柱：**{return_bikes}** 格")
            else:
                st.error("API 請求失敗，無法取得資料。")                
        except Exception as e:
            st.error(f"網路連線發生錯誤: {e}")
