---
title: "How Databricks can help with real time analytics"
author: "Akshay Gulabrao"
date : "2025 September 26"
bibliography: databricks_references.bib
link-citations: true
---
[Home](./index.html)


In this tutorial, I will be demonstrating how to use databricks to extract real-time insights from raw data. As an example, I will be extracting raw weather observations from weather stations around the US. A potential use-case is demand forecasting, or trading in prediction markets. We will begin with visualizing the real time data and eventually use it to train a self-supervised learning model to predict future raw weather observations. 

Databricks builds ETL pipelines around a **data lakehouse**. 