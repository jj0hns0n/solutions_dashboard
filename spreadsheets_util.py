try: 
  from xml.etree import ElementTree
except ImportError:  
  from elementtree import ElementTree
import gdata.docs.data
import gdata.docs.client
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import string

def PromptForSpreadsheet(gd_client):
  # Get the list of spreadsheets
  feed = gd_client.GetSpreadsheetsFeed()
  PrintFeed(feed)
  input = raw_input('\nSelection: ')
  return feed.entry[string.atoi(input)].id.text.rsplit('/', 1)[1]

def PrintFeed(feed):
  for i, entry in enumerate(feed.entry):
    if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
      print '%s %s\n' % (entry.title.text, entry.content.text)
    elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
      print '%s %s %s' % (i, entry.title.text, entry.content.text)
      # Print this row's value for each column (the custom dictionary is
      # built from the gsx: elements in the entry.) See the description of
      # gsx elements in the protocol guide.
      print 'Contents:'
      for key in entry.custom:
        print '  %s: %s' % (key, entry.custom[key].text)
      print '\n',
    else:
      print '%s %s\n' % (i, entry.title.text)

def PromptForWorksheet(gd_client, key):
  # Get the list of worksheets
  feed = gd_client.GetWorksheetsFeed(key)
  PrintFeed(feed)
  input = raw_input('\nSelection: ')
  return feed.entry[string.atoi(input)].id.text.rsplit('/', 1)[1]

def ListInsertAction(gd_client, key, wksht_id, row_data):
  entry = gd_client.InsertRow(row_data, key, wksht_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print 'Inserted!'

def ListUpdateAction(gd_client, key, wksht_id, index, row_data):
  feed = gd_client.GetListFeed(key, wksht_id)
  entry = gd_client.UpdateRow(
      feed.entry[string.atoi(index)],
      row_data)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    pass
    #print 'Updated!'

def StringToDictionary(row_data):
  result = {}
  for param in row_data.split():
    name, value = param.split('=')
    result[name] = value
  return result

def CellsUpdateAction(gd_client, key, wksht_id, row, col, inputValue):
  entry = gd_client.UpdateCell(row=row, col=col, inputValue=inputValue, 
      key=key, wksht_id=wksht_id)
  #if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
  #  print 'Updated!'
