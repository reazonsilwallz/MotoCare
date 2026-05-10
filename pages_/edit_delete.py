import streamlit as st
import altair as alt
import pandas as pd
from datetime import date, datetime
from helpers import get_vehicles, get_records, records_df, save_data, CATEGORIES