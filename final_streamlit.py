import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
from streamlit_option_menu import option_menu
#reading the csv file
df1=pd.read_csv("Airbnb.csv")
def sun(a):
    if(a=="All"):
        df=df1
    else:
        country=a
        df=df1[df1["Country"]==country]
    fig_2 = px.sunburst(df, 
                    path=['Country','Street','Property_type','Room_type','Name'], 
                    values='Review_scores',
                    color_discrete_sequence=px.colors.qualitative.Prism,  # Example color palette
                    maxdepth=3,  # Limit the depth of the sunburst to make it clearer
                    # labels={amount},  # Update labels for clarity
                    title="Sunburst Chart for Transactions",  # Add a title
                    height=850,  # Set the height of the chart
                    width=850,  # Set the width of the chart
                    )
    fig_2.update_traces(textfont=dict(size=12), insidetextorientation='radial')  # Adjust font size and text orientation
    fig_2.update_layout(margin=dict(t=0, l=0, r=0, b=0),  # Remove unnecessary margins
                        plot_bgcolor='rgba(0,0,0,0)')  # Set transparent background
    return fig_2
def map():
    # fig = px.choropleth(
    #             df1,
    #             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    #             featureidkey='properties.ST_NM',
    #             locations='Country',
    #             color="Street",
    #             # title=f"year {i} Quarter {j}",
    #             color_continuous_scale='Blue',
    #             # range_color=(0,b[count].max()),  # Define the range of colors
    #             height=700,
    #             width=700
    #         )
    # fig.update_geos(fitbounds="locations", visible=False)
    fig = px.choropleth(df1, locations='Country', locationmode='country names',
                    color_discrete_sequence=['#636EFA'],  # Color for the highlighted countries
                    title='Highlighted Countries Map')
# Update layout for better visualization
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        title_x=0.5
    )
    return fig
import plotly.express as px
def glo():
    fig = px.scatter_mapbox(df1, 
                            lat="Latitude", 
                            lon="Longitude", 
                            color="availability_365",
                            size="availability_365",  # Adjust marker size based on availability
                            hover_name="Country",
                            hover_data={"suburb": True, "market": True, "Country": True, "availability_365": True},
                            color_continuous_scale=px.colors.sequential.Viridis,
                            zoom=1,
                            width=1300,
                            height=700)
    
    fig.update_layout(mapbox_style="open-street-map", 
                    title="Listing Availability by Location",
                    title_font=dict(size=24, family='Arial', color='red'),  # Enhance title
                    margin={"r":0,"t":50,"l":0,"b":0},  # Adjust margins for better layout
                    coloraxis_colorbar=dict(
                        title="Availability (days)",
                        ticks="outside",
                        tickvals=[0, 100, 200, 300, 365],
                        ticktext=["0", "100", "200", "300", "365"],
                        lenmode="fraction", len=0.5,
                    )) 
    
    fig.update_traces(marker=dict(opacity=0.7, sizemode='area', sizemin=4))  # Make markers semi-transparent and minimum size
    
    return fig
def bar_chart():
    df=df1.groupby("Country")["availability_365"].mean()
    d=pd.DataFrame(df)
    d.reset_index(inplace=True)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=d['Country'], 
        y=d['availability_365'], 
        marker_color='indianred',  # Set bar color
        text=d['Country'],  # Display value on bars
        textposition='auto'
    ))

    fig.update_layout(
        title="Bar Chart Example",
        title_font=dict(size=24, family='Arial', color='green'),
        xaxis_title="Country",
        yaxis_title="Average Availability in a year",
        margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins
        xaxis=dict(tickangle=-45),  # Rotate x-axis labels if necessary
    )
    return fig
def pie_line(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    f=[]
    df=d.groupby("Property_type")['Review_scores'].count()
    k=pd.DataFrame(df)
    k.reset_index(inplace=True)
    k.columns = ["Property_type","count"]
    fig = px.pie(k,values="count",names="Property_type", title=f'User Count Distribution by Region')
    # Update traces to show labels
    fig.update_traces(textinfo='label+percent')

    # Optionally, you can customize the position of the labels
    fig.update_traces(textposition='inside')
    f.append(fig)
    r=[True,False]
    for i in r:
        z=k.sort_values(by="count",ascending=i)
        b=z.head()
        fig_1 = go.Figure()

        fig_1.add_trace(go.Bar(
            x=b['Property_type'], 
            y=b['count'], 
            marker_color='orange',  # Set bar color
            text=b['Property_type'],  # Display value on bars
            textposition='auto'
        ))

        fig_1.update_layout(
            title="Bar Chart Example",
            title_font=dict(size=24, family='Arial', color='darkblue'),
            xaxis_title="Category",
            yaxis_title="Value",
            margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins
            xaxis=dict(tickangle=-45),  # Rotate x-axis labels if necessary
        )
        f.append(fig_1)
    return f
def box(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    fig = px.box(d, x="Room_type", y="availability_365", title="Box plot of Room types by Availability")
    fig2 = px.box(d, x="Room_type", y="Review_scores", title="Box plot of Room types by Review Score")
    f=[fig,fig2]
    return f
def sc(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    fig = px.scatter(d, x="Bed_type", y="Review_scores", title="Scatter plot of Bed type vs Review score")
    return fig
def card(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    list=["Min_nights","Max_nights","Cleaning_fee","Review_scores_accuracy","Review_scores_cleanliness","Review_scores_checkin","Review_scores_communication","Review_scores_location","Review_scores_value","Review_scores_rating"]
    color=["sandybrown","seagreen","blue","sienna","red","skyblue","slateblue","slategray","slategrey","orange"]
    f=[]
    for i,j in zip(list,color):
        # Create a blank figure
        fig = px.scatter()
        a=i
        b=d[i].mean()
        # Update layout to add a card-like annotation
        fig.update_layout(
            annotations=[
                dict(
                    text=f"{a}<br><b>{b}",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=20),
                    align="center",
                    bordercolor="black",
                    borderwidth=2,
                    borderpad=10,
                    bgcolor=j,
                    opacity=0.8
                )
            ],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            width=300,
            height=200,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        f.append(fig)
    return f
def heat(a):
    if(a=="All"):
        d=df1
    else:
        country=a
        d=df1[df1["Country"]==country]
    x=d[["Review_scores","Review_scores_communication","Review_scores_checkin","Review_scores_location","Review_scores_value","Review_scores_rating"]]
    # Compute the correlation matrix
    corr_matrix = x.corr()

    # Create a heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='tempo',
        zmin=0, zmax=1
    ))
    # tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid','turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd'
    # Add annotations
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            fig.add_annotation(
                x=corr_matrix.columns[j],
                y=corr_matrix.columns[i],
                text=str(round(corr_matrix.iloc[i, j], 2)),
                showarrow=False,
                font=dict(color="black" if abs(corr_matrix.iloc[i, j]) < 0.5 else "white")
            )

    # Update layout for better appearance
    fig.update_layout(
        title='Correlation Matrix Heatmap',
        xaxis_nticks=25,
        yaxis_nticks=25,
        width=1200,  # Increase width
        height=600 
    )

    return fig
def fun(z):
        st.plotly_chart(sun(z))
        col1, col2 = st.columns(2)
        a=pie_line(z)
        with col2:
            t1,t2=st.tabs(["top 5","buttom 5"])
            # Chart 1: Bar chart
            with t2:
                    st.plotly_chart(a[1])

            # Chart 2: Pie chart
            with t1:
                    st.plotly_chart(a[2])
        with col1:
            st.plotly_chart(a[0])
        st.plotly_chart(heat(z))
        c=card(z)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.plotly_chart(c[0])
        with col2:
            st.plotly_chart(c[1])
        with col3:
            st.plotly_chart(c[2])
        with col4:
            st.plotly_chart(c[3])
        b=box(z)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(b[0])
        with col2:
            st.plotly_chart(b[1])
        st.plotly_chart(sc(z))
        col1,col2,col3,col4= st.columns(4)
        with col1:
            st.plotly_chart(c[4])
        with col2:
            st.plotly_chart(c[5])
        with col3:
            st.plotly_chart(c[6])
        with col4:
            st.plotly_chart(c[7])
        col5,col6= st.columns(2)
        with col5:
            st.plotly_chart(c[8])
        with col6:
            st.plotly_chart(c[9])
        return(0)






























#streamli page
st.set_page_config(layout="wide")

with st.sidebar:
    select_option=option_menu("Menu",["About","Map","Insights"])
if select_option=="About":
    image1 ="data:image/png;base64,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"
    st.image(image1, caption="Airbnb Logo")
    # Page Title
    st.title("Discover Airbnb")

    # Introduction
    st.markdown("""
    Airbnb is an online marketplace that connects people who want to rent out their homes with those who are looking for accommodations. Founded in 2008, Airbnb has grown to become one of the leading platforms for short-term rentals, offering unique and diverse lodging options around the world.
    """)

    # Load Images
    image2 ="data:image/jpeg;base64,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"
    image3 = "data:image/jpeg;base64,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"

    # Display Images
    c1,c2=st.columns(2)
    with c1:
        st.image(image2, width=600)
    with c2:
        st.image(image3,width=600)

    # Airbnb's Story
    st.header("The Story of Airbnb")
    st.markdown("""
    Airbnb was founded by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. The idea was born out of necessity when they decided to rent out air mattresses in their San Francisco apartment to make extra money. The concept quickly evolved into a full-fledged business that disrupted the traditional hospitality industry.

    Key milestones in Airbnb's journey:
    - **2008**: Airbnb is founded in San Francisco.
    - **2011**: Reaches 1 million nights booked.
    - **2014**: Expands to over 1 million listings worldwide.
    - **2020**: Airbnb goes public.

    Airbnb allows travelers to experience cities like a local by staying in unique accommodations, ranging from apartments and houses to castles and treehouses. Hosts can share their spaces and earn income, while guests benefit from more affordable and personalized lodging options.
    """)

    # Airbnb's Offerings
    st.header("What Airbnb Offers")
    st.markdown("""
    Airbnb's platform offers a variety of services, including:
    - **Homes**: Rent unique homes and apartments around the world.
    - **Experiences**: Participate in activities hosted by locals, such as cooking classes, tours, and adventures.
    - **Adventures**: Multi-day trips and experiences curated by experts.

    Airbnb also provides options for long-term stays and business travel accommodations, catering to different types of travelers.
    """)

    # Conclusion
    st.header("Join the Community")
    st.markdown("""
    Whether you're looking for a place to stay, an unforgettable experience, or a way to earn extra income by hosting, Airbnb has something for everyone. Join millions of hosts and guests who are part of the Airbnb community today.
    """)
    url = "https://community.withairbnb.com/t5/Community-Center/ct-p/community-center"
    label = "Airbnb Community"

    # Create a styled link with a border
    st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 10px; display: inline-block; border-radius: 5px;">
            <a href="{url}" target="_blank" style="text-decoration: none; color: #4CAF50; font-weight: bold;">
                {label}
            </a>
        </div>
    """, unsafe_allow_html=True)

    

elif select_option=="Map":
    st.plotly_chart(glo())
elif select_option=="Insights":
    st.plotly_chart(bar_chart())
    country=st.selectbox("Country:",['All countries','United States', 'Turkey', 'Hong Kong', 'Australia', 'Portugal','Brazil', 'Canada', 'Spain', 'China'])
    if country=="All countries":
        fun("All")
    elif country=="United States":
        fun("United States")
    elif country=="Turkey":
        fun("Turkey")        
    elif country=="Hong Kong":
        fun("Hong Kong")        
        
    elif country=="Australia":
        fun("Australia")
    elif country=="Portugal":
        fun("Portugal")
        
    elif country=="Brazil":
        fun("Brazil")
        
    elif country=="Canada":
        fun("Canada")
        
    elif country=="Spain":
        fun("Spain")
        
    elif country=="China":
        fun("China")
        
