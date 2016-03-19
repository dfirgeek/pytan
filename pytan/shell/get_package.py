from . import base


class Worker(base.Base):
    DESCRIPTION = 'Get package information and export to a report file'
    GROUP_NAME = 'Package Search Options'
    ACTION = 'package'
    PREFIX = 'get_package'

    def setup(self):
        self.grp = self.parser.add_argument_group(self.GROUP_NAME)

        self.grp.add_argument(
            '-s', '--search',
            required=False, action='append', default=[], dest='search',
            help='Searchable text string for finding packages'
        )
        self.add_help_opts()
        self.add_export_results_opts()
        self.add_report_opts()
        self.grp_choice_results()

    def get_response(self, kwargs):
        grps = [self.GROUP_NAME]
        kwargs = self.get_parser_args(grps)
        m = "++ Getting packages with search items:\n{}"
        print(m.format(self.pf(kwargs)))
        response = self.handler.get_packages(**kwargs)
        self.handler.MYLOG.debug("{}".format(response))
        return response

    def get_result(self):
        grps = ['Export Results Options', 'Export Object Options', 'Report File Options']
        kwargs = self.get_parser_args(grps)
        response = self.get_response(kwargs)
        if response:
            report_file, result = self.handler.export(response, **kwargs)
            return response, report_file, result
        else:
            print("!! No value found for search items.")
