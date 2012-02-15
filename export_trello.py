import os
from trollop import TrelloConnection

# Get a temporary Token here https://trello.com/1/appKey/generate
# https://trello.com/1/appKey/generate#

opengeo_id = '4ea6f4dc1c72a165b685f569'

trello_conn = TrelloConnection(os.environ['TRELLO_API_KEY'], os.environ['TRELLO_TOKEN'])

# By Organization
opengeo_org = trello_conn.get_organization(opengeo_id)
org_members = opengeo_org.members
for member in org_members:
    print member.username
    for card in member.cards:
        print "\t", card.name, card.board.name, card.list.name

# By Board
boards = trello_conn.me.boards
for board in boards:
    print board.name
    for checklist in board.checklists:
        print checklist.name, checklist.cards, len(checklist.checkitems)
        for checkitem in checklist.checkitems:
            print checkitem['name']
    for list in board.lists:
        print "\t", list.name
        for card in list.cards:
            print "\t\t", card.name
            for checkitem in card.checkItemStates:
                print "\t\t\t", checkitem
            for member in card.members:
                print "\t\t\t", member.username

