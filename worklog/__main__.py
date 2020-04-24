import logging

import worklog.command
import worklog.config
import worklog.report
import worklog.task
import worklog.trello.client
import worklog.trello.config
import worklog.trello.url

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)s] %(message)s',
)
log = logging.getLogger(__name__)


def main():
    args = worklog.command.Args()
    cfg = worklog.config.Params(args)
    trello_urls = worklog.trello.url.Builder(cfg.trello)
    trello = worklog.trello.client.Session(cfg.trello, trello_urls)
    board = trello.get_board()
    lists = trello.get_lists(board)
    cards = trello.get_cards(board)
    builder = worklog.report.Builder(cfg, lists, cards)
    reports = (builder.jira(), builder.human(), builder.summary())
    for report in reports:
        print('#' * 80)
        print(report)


if __name__ == '__main__':
    main()
