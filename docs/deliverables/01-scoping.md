# Project Scoping (10%, max 1 page, due Friday Week 4)

**Group members:** Uvidu De Silva (23101016), Nelson Cololo Onodugo (23508), Alexander Zudins (32141), Tawana Gumede (44520), Mohammed Mohammed Arfhan (21111), Cameron Jake Servitillo (21336)

## Purpose

The purpose of this app is to improve the process of recovering lost items at DCU by developing an LLM-based lost and found service. The system will help students retrieve lost items efficiently by using an LLM-based agent to extract structured details from item descriptions and match lost items against found items.

## Scope

DCU Lost & Found is a standalone web application built for DCU students. When a student finds an item, they upload a photo and enter a description — for example: "Black Nike water bottle found outside the library." The student brings the item to the DCU Lost & Found room, and the LLM agent extracts structured attributes (object, colour, brand, location, features) from the description and stores them in the database.

If a student loses an item, they can enter a description such as: "I lost my black Nike bottle near the library." The agent compares this against stored found-item records using semantic similarity — not exact keyword matching — and displays ranked matching items with their images, helping students quickly identify and recover their belongings.

## Goals

- Reduce the time and effort needed for a student to recover a lost item
- Replace inconsistent manual logging with structured, automatically-extracted item records
- Demonstrate an LLM agent applied to a genuine DCU problem, using prompt-based extraction and semantic matching

## Deliverables

- **Django-based web application** — builds and runs the Lost & Found system
- **LLM-based agent** — extracts structured details from item descriptions and matches lost items against found items
- **MySQL database** — stores lost and found item records
- **Interactive, user-friendly interface** following standard web design principles
