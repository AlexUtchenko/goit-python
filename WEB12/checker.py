import aiohttp
import asyncio
import datetime




AQI_SEB = {}
KP_NOAA = {}
UV = {}
UV_OWM = {}




async def air_quality(session):
    global AQI_SEB
    url = 'https://api.saveecobot.com/output.json'
    results = []
    async with session.get(url) as response:
        rows = await response.json()
        for i in rows:
            if i["cityName"] == "Brovary" and i["stationName"] == "vulytsia Oleksiia Bolshechenka, 7" or i["cityName"] == "Brovary" and i["stationName"] == "bulvar Nezalezhnosti, 4A":
                for pol in i['pollutants']:
                    if pol['pol'] == 'Air Quality Index':
                        results.append(int(pol['value']))
                        AQI_SEB[i["stationName"]] = int(pol['value'])
        AQI_SEB["AVG"] = sum(results) / len(results)
        if AQI_SEB["AVG"] <= 50:
            AQI_SEB["description"] = 'good'
        elif 51 <= AQI_SEB["AVG"] <= 100:
            AQI_SEB["description"] = 'moderate'
        elif 101 <= AQI_SEB["AVG"] <= 150:
            AQI_SEB["description"] = 'harmful for sensitive'
        elif 151 <= AQI_SEB["AVG"] <= 200:
            AQI_SEB["description"] = 'harmful'
        elif 201 <= AQI_SEB["AVG"] <= 300:
            AQI_SEB["description"] = 'very harmful'
        elif AQI_SEB["AVG"] > 300:
            AQI_SEB["description"] = '!!!DANGER!!!'


async def kp_index_noaa(session):
    global KP_NOAA
    url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
    async with session.get(url) as response_kp:
        rows = await response_kp.json()
        kp_sum = 0
        for row in rows:
            kp_sum += int(row["kp_index"])
        KP_NOAA["KP_NOAA_AVG_2H"] = round(kp_sum/len(rows))
        if KP_NOAA["KP_NOAA_AVG_2H"] < 4:
            KP_NOAA["KP_NOAA_description"] = "normal (green)"
        elif KP_NOAA["KP_NOAA_AVG_2H"] == 4:
            KP_NOAA["KP_NOAA_description"] = "warning(orange)"
        elif KP_NOAA["KP_NOAA_AVG_2H"] >= 5:
            KP_NOAA["KP_NOAA_description"] = "storm (red)"


async def uv_index(session):
    global UV
    url = f'https://api.openuv.io/api/v1/uv?lat=50.51&lng=30.79&dt={datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}'
    headers = {'content-type': 'application/json', 'x-access-token': 'TOKEN'}
    async with session.get(url, headers=headers) as response_uv:
        rows = await response_uv.json()
        UV['UV'] = float(rows['result']['uv'])
        UV['ozone'] = float(rows['result']['ozone'])
        UV['ozone_time'] = rows['result']['ozone_time']
        UV['uv_max'] = float(rows['result']['uv_max'])
        UV['uv_max_time'] = rows['result']['uv_max_time']
        if 0 <= UV['UV'] < 3:
            UV['description'] = 'Low'
        elif 3 <= UV['UV'] < 6:
            UV['description'] = 'Moderate'
        elif 6 <= UV['UV'] < 8:
            UV['description'] = 'High'
        elif 8 <= UV['UV'] < 11:
            UV['description'] = 'Very high'
        elif UV['UV'] > 11:
            UV['description'] = 'Extreme'


async def uv_index_openweathermap(session):
    global UV_OWM
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat=50.51&lon=30.79&exclude=minutely,alerts&appid=TOKEN'
    async with session.get(url) as response_uv_owm:
        rows = await response_uv_owm.json()
        UV_OWM["UVI"] = rows['current']['uvi']
        temp_res = []
        for hour in rows['hourly']:
            temp_res.append(hour['uvi'])
        UV_OWM["UVI_MAX_for_48h"] = max(temp_res)
        if 0 <= UV_OWM['UVI'] < 3:
            UV_OWM['description'] = 'Low'
        elif 3 <= UV_OWM['UVI'] < 6:
            UV_OWM['description'] = 'Moderate'
        elif 6 <= UV_OWM['UVI'] < 8:
            UV_OWM['description'] = 'High'
        elif 8 <= UV_OWM['UVI'] < 11:
            UV_OWM['description'] = 'Very high'
        elif UV_OWM['UVI'] > 11:
            UV_OWM['description'] = 'Extreme'


async def check_warnings():
    global AQI_SEB, KP_NOAA, UV, UV_OWM
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(air_quality(session), kp_index_noaa(session))
        # await asyncio.gather(
        #     air_quality(session), kp_index_noaa(session), uv_index(session), uv_index_openweathermap(session)
        # )
    if AQI_SEB['AVG'] > 100:
        print(f"!!! WARNING !!! {datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\nAir pollution! AQI: {AQI_SEB['description']}\nAQI_avg_value: {AQI_SEB['AVG']}\n")
    elif KP_NOAA['KP_NOAA_description'] != 'normal (green)':
        print(f"!!! WARNING !!! {datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\nGeomagnetic activity! K-index: {KP_NOAA['KP_NOAA_description']}")
    elif UV['description'] != 'Low':
        print(f"!!! WARNING !!! {datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\nUV radiation! UV-index(ouv): {UV['description']}")
    elif UV_OWM['description'] != 'Low':
        print(f"!!! WARNING !!! {datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\nUV radiation! UV-index(owm): {UV_OWM['description']}")
    else:
        print('no warning')
    await asyncio.sleep(20)




if __name__ == "__main__":
    while True:
        asyncio.run(check_warnings())











