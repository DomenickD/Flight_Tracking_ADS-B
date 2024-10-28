"""VIZ Page for Streamlit Airport ADSB project"""

import streamlit as st


st.subheader("ADS-B Visualizations")

st.divider()

st.image(r"Pictures/Heatmap_flaw.png")
st.caption(
    "This image shows the flaws in the ADS-B data that were pulled. \
    If more time allowed, this data would be parses so each column was \
    limited to a smaller range of data to help the model. "
)

st.divider()

st.image(r"Pictures/500_nm_Tampa.png")
st.caption(
    "Here we see the API pull with 500nm from Tampa. \
    You can clearly see the spaces with the least and most flight traffic. "
)

st.divider()

st.image(r"Pictures/50_nm_Tampa.png")
st.caption(
    "Here we see the API pull with 50nm from Tampa. \
    You can see how busy Tampa is, but this is also pulled over a longer period."
)

st.divider()

st.image(r"Pictures/corr_airport.png")
st.caption("We want to focus on the bottom two rows here. ")

st.divider()

st.image(r"Pictures/heading_bar.png")
st.caption(
    "Heading refers to the direction in which the nose of the aircraft is pointed,\
     expressed in degrees relative to true north. It is measured clockwise from 0° \
           (north) through 360°.\
    when all of the data is between 0 and 6 degrees, it indicates that the aircraft \
           is pointed almost directly north."
)
