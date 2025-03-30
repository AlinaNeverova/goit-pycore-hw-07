# CLI Assistant Bot

This is a simple command-line assistant bot for managing a contact book.  
It allows you to add, edit, and delete contacts, phone numbers, and birthdays.  
The bot also tracks upcoming birthdays within the next 7 days.

## Features
- Add/edit/delete contacts and phone numbers
- Add/show birthdays with date validation
- Show all contacts
- Show upcoming birthdays (auto-adjusts for weekends)
- Friendly error handling via decorators

## Usage
Run the bot and interact via text commands like:
- `add John 0123456789`
- `change John 0123456789 0987654321`
- `add-birthday John 01.04.1999`
- `birthdays`
- `all`
- `exit`

## Format requirements
- Phone numbers: 10 digits only
- Birthdays: `DD.MM.YYYY`
