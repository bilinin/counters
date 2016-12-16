########## EXCEL
import xlrd
import xlutils.copy

def _getOutCell(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK

def make_report(bd):
    offset = 9
    inBook = xlrd.open_workbook('Report230.xls', formatting_info=True)
    outBook = xlutils.copy.copy(inBook)
    outSheet = outBook.get_sheet(0)
    i =0
    for current in bd:
        setOutCell(outSheet , 1, i+offset, bd[current]['label'])
        setOutCell(outSheet, 3, i + offset, int(bd[current]['nt']))
        setOutCell(outSheet , 6, i+offset, bd[current]['energy'])

        i += 1
    outBook.save('output.xls')
########## EXCEL