# Fodboldtur---GUI
GUI support for existing Fodboldtur assignment.


### TODO-LIST
As of 14-02-2023 and ahead.

- [x] Collect the "indbetaling" and "udbetaling" buttons into one "transaction" button
- [x] Display the owed amount for each person in the "resterende beløb" column of the treeview
- [ ] Fix integer and floating number stuff - perhaps with some string magic; one for the int-number and one for the decimals
- [ ] Fix button layout and sizing
- [x] Create settings menu/frame
  - [ ] Turn logging on/off
  - [x] Filter log
    - [x] Save messages
    - [x] Action messages
    - [x] Data loaded successfully messages
  - [ ] Autosave
- [ ] Create progress bar for pay-goal
- [ ] Clean up code
  - [ ] Get rid of the atrocious useless class for tkinter stuff


### Complete feature-list
1. Make transactions for registered members. Both in and out of the accounts.
2. Add new members with a starting amount. Adding new members updates each person debt; the total debt divided with the new amount of members.
3. Remove members. Removing members also updates each person debt.
4. Show the leaderboard of shame with the 3 people who've paid the least.
5. Settings window with settings for saving and logging. 
6. Complete Logging systems with a filter for log-types in the settings.
7. Autosave with a toggle-switch in the settings.
8. Progress bar and text displaying the progress towards the pay-goal.