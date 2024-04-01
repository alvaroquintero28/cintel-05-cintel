import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # this package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req


# use the built in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# names the page
ui.page_opts(title="Alvaro's King Penguin data", fillable=True)

# creates sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],)

    # Add a second selectize to make scatterplot interactive
    ui.input_selectize(
        "second_selected_attribute",
        "Select Scatterplot Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    # Creates a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 20)
    
    # Creates a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 50)
    
    # Creates a checkbox group input
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,)
    
    ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
         penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=True,)


      # Adds a horizontal rule to the sidebar
    ui.hr()
    
    # Adds a hyperlink to GitHub Repo
    ui.a(
        "GitHub",
         href="https://github.com/alvaroquintero28/cintel-02-data/blob/main/app.py",
         target="_blank",
         )
   
# create a layout to include 2 cards with a data table and data grid
with ui.layout_columns():
    with ui.card(full_screen=True):  # full_screen option to view expanded table/grid
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data())

    with ui.card(full_screen=True):  # full_screen option to view expanded table/grid
        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())

# added a horizontal rule
ui.hr()

# create a layout to include 3 cards with different plots
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Species Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.card(full_screen=True):
        ui.h2("Species Seaborn Histogram")

        @render.plot(alt="Species Seaborn Histogram")
        def seaborn_histogram():
            seaborn_plot = sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                multiple="dodge",
                hue="species",
            )
            seaborn_plot.set_title("Species Seaborn Histogram")
            seaborn_plot.set_ylabel("Measurement")

    with ui.card(full_screen=True):
        ui.h2("Species Plotly Scatterplot")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                title="Plotly Scatterplot",
                x=input.selected_attribute(),
                y=input.second_selected_attribute(),
                color="species",
                symbol="species",
            )

@reactive.calc
def filtered_data():
    return penguins_df[(penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))]

