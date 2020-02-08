#!/bin/python3


def process_bar_text(spider_name, total, totals, succeed, error):
    num_arrow = int(total / totals * 50)
    num_line = 50 - num_arrow
    return 'Current Spider site: [ %s ]' % spider_name + '  Process: %s-%s' % (total, totals) + '  [' + '>' * num_arrow + ' ' * num_line + ']' + '  rate: %.2f' % (total / totals * 100) + '%    succeed: ' + str(succeed) + '; error: ' + str(error) + '\r'
