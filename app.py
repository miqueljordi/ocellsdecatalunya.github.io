from flask import Flask, render_template, request
import pandas as pd
import folium

app = Flask(__name__)

# Read the TSV file into a pandas DataFrame
df = pd.read_csv("ebd_ES-CT-GN_202301_202312_smp_relDec-2023.txt", sep='\t')

columns_to_remove = ['GLOBAL UNIQUE IDENTIFIER', 'TAXONOMIC ORDER', 'CATEGORY', 'TAXON CONCEPT ID', 'SUBSPECIES COMMON NAME', 'SUBSPECIES SCIENTIFIC NAME', 'EXOTIC CODE',
                     'BREEDING CODE', 'BREEDING CATEGORY', 'BEHAVIOR CODE', 'AGE/SEX', 'COUNTRY', 'STATE CODE', 'STATE CODE',
                     'IBA CODE', 'BCR CODE', 'NUMBER OBSERVERS', 'ALL SPECIES REPORTED', 'GROUP IDENTIFIER', 'HAS MEDIA', 'REASON', 'TRIP COMMENTS', 'SPECIES COMMENTS', 'Unnamed: 49',
                     'USFWS CODE', 'ATLAS BLOCK', 'OBSERVER ID', 'SAMPLING EVENT IDENTIFIER', 'PROTOCOL TYPE', 'PROTOCOL CODE', 'PROJECT CODE', 'DURATION MINUTES',
                     'EFFORT DISTANCE KM', 'EFFORT AREA HA', 'APPROVED', 'REVIEWED', 'LAST EDITED DATE', 'TIME OBSERVATIONS STARTED', 'COUNTY CODE', 'LOCALITY ID', 'LOCALITY TYPE']
# Remove specified columns
df.drop(columns=columns_to_remove, inplace=True)

# Convert 'OBSERVATION DATE' to datetime format if it's not already in datetime
if df['OBSERVATION DATE'].dtype != 'datetime64[ns]':
    df['OBSERVATION DATE'] = pd.to_datetime(df['OBSERVATION DATE'])

# Function to create the map
def create_map(species, start_date, end_date):
    # Filter DataFrame based on selected species and date range
    filtered_df = df[df['COMMON NAME'] == species]
    if start_date:
        filtered_df = filtered_df[filtered_df['OBSERVATION DATE'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['OBSERVATION DATE'] <= end_date]
    
    # Create a map if there are observations for the selected species and date range
    if not filtered_df.empty:
        # Create a map centered at the mean latitude and longitude of observations
        map_center = [filtered_df['LATITUDE'].mean(), filtered_df['LONGITUDE'].mean()]
        m = folium.Map(location=map_center, zoom_start=8)
        
        # Add markers for each observation
        for _, row in filtered_df.iterrows():
            # Define popup content with locality and observation date
            popup_content = f"Locality: {row['LOCALITY']}<br>Date: {row['OBSERVATION DATE'].strftime('%Y-%m-%d')}"
            folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=popup_content).add_to(m)
        
        # Save the map as an HTML file
        m.save("templates/map.html")

@app.route('/')
def index():
    all_species = df['COMMON NAME'].unique().tolist()
    return render_template('index.html', all_species=all_species)


@app.route('/map', methods=['GET', 'POST'])
def map():
    species = request.args.get('species')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    create_map(species, start_date, end_date)
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
