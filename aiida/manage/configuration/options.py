# -*- coding: utf-8 -*-
"""Definition of known configuration options and methods to parse and get option values."""
from __future__ import absolute_import

import collections
import six

__all__ = ('get_option', 'get_option_names', 'parse_option')


class NO_DEFAULT_PLACEHOLDER(object):
    """A dummy class to serve as a marker for no default being specified in the `get_option` function."""
    # pylint: disable=too-few-public-methods,invalid-name
    pass


NO_DEFAULT = NO_DEFAULT_PLACEHOLDER()
DEFAULT_DAEMON_TIMEOUT = 20  # Default timeout in seconds for circus client calls
VALID_LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'REPORT', 'INFO', 'DEBUG']

Option = collections.namedtuple('Option', ['name', 'key', 'valid_type', 'valid_values', 'default', 'description'])


def get_option(option_name):
    """Return a configuration option.configuration

    :param option_name: the name of the configuration option
    :return: the configuration option
    :raises ValueError: if the configuration option does not exist
    """
    try:
        option = Option(option_name, **CONFIG_OPTIONS[option_name])
    except KeyError:
        raise ValueError('the option {} does not exist'.format(option_name))
    else:
        return option


def get_option_names():
    """Return a list of available option names.

    :return: list of available option names
    """
    return CONFIG_OPTIONS.keys()


def parse_option(option_name, option_value):
    """Parse and validate a value for a configuration option.

    :param option_name: the name of the configuration option
    :param option_value: the option value
    :return: a tuple of the option and the parsed value
    """
    option = get_option(option_name)

    value = False

    if option.valid_type == 'bool':
        if isinstance(option_value, six.string_types):
            if option_value.strip().lower() in ['0', 'false', 'f']:
                value = False
            elif option_value.strip().lower() in ['1', 'true', 't']:
                value = True
            else:
                raise ValueError('option {} expects a boolean value'.format(option.name))
        else:
            value = bool(option_value)
    elif option.valid_type == 'string':
        value = six.text_type(option_value)
    elif option.valid_type == 'int':
        value = int(option_value)
    elif option.valid_type == 'list_of_str':
        value = option_value.split()
    else:
        raise NotImplementedError('Type string {} not implemented yet'.format(option.valid_type))

    if option.valid_values is not None:
        if value not in option.valid_values:
            raise ValueError('{} is not among the list of accepted values for option {}'.format(value, option.name))

    return option, value


CONFIG_OPTIONS = {
    'runner.poll.interval': {
        'key': 'runner_poll_interval',
        'valid_type': 'int',
        'valid_values': None,
        'default': 1,
        'description': 'The polling interval in seconds to be used by process runners',
    },
    'daemon.timeout': {
        'key': 'daemon_timeout',
        'valid_type': 'int',
        'valid_values': None,
        'default': DEFAULT_DAEMON_TIMEOUT,
        'description': 'The timeout in seconds for calls to the circus client',
    },
    'verdishell.modules': {
        'key': 'modules_for_verdi_shell',
        'valid_type': 'string',
        'valid_values': None,
        'default': '',
        'description': 'Additional modules/functions/classes to be automatically loaded in `verdi shell`',
    },
    'verdishell.calculation_list': {
        'key': 'projections_for_calculation_list',
        'valid_type': 'list_of_str',
        'valid_values': None,
        'default': ('pk', 'ctime', 'process_state', 'type', 'job_state'),
        'description': 'List of default projections for `verdi calculation list`',
    },
    'logging.aiida_loglevel': {
        'key': 'logging_aiida_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'REPORT',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `aiida` logger',
    },
    'logging.db_loglevel': {
        'key': 'logging_db_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'REPORT',
        'description': 'Minimum level to log to the DbLog table',
    },
    'logging.tornado_loglevel': {
        'key': 'logging_tornado_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `tornado` logger',
    },
    'logging.plumpy_loglevel': {
        'key': 'logging_plumpy_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `plumpy` logger',
    },
    'logging.kiwipy_loglevel': {
        'key': 'logging_kiwipy_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `kiwipy` logger',
    },
    'logging.paramiko_loglevel': {
        'key': 'logging_paramiko_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `paramiko` logger',
    },
    'logging.alembic_loglevel': {
        'key': 'logging_alembic_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `alembic` logger',
    },
    'logging.sqlalchemy_loglevel': {
        'key': 'logging_sqlalchemy_loglevel',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'WARNING',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `sqlalchemy` logger',
    },
    'logging.circus_loglevel': {
        'key': 'logging_circus_log_level',
        'valid_type': 'string',
        'valid_values': VALID_LOG_LEVELS,
        'default': 'INFO',
        'description': 'Minimum level to log to daemon log and the `DbLog` table for the `circus` logger',
    },
    'tcod.depositor_username': {
        'key': 'tcod_depositor_username',
        'valid_type': 'string',
        'valid_values': None,
        'default': NO_DEFAULT,
        'description': 'Username for TCOD deposition',
    },
    'tcod.depositor_password': {
        'key': 'tcod_depositor_password',
        'valid_type': 'string',
        'valid_values': None,
        'default': NO_DEFAULT,
        'description': 'Password for TCOD deposition',
    },
    'tcod.depositor_email': {
        'key': 'tcod_depositor_email',
        'valid_type': 'string',
        'valid_values': None,
        'default': NO_DEFAULT,
        'description': 'E-mail address for TCOD deposition',
    },
    'tcod.depositor_author_name': {
        'key': 'tcod_depositor_author_name',
        'valid_type': 'string',
        'valid_values': None,
        'default': NO_DEFAULT,
        'description': 'Author name for TCOD depositions',
    },
    'tcod.depositor_author_email': {
        'key': 'tcod_depositor_author_email',
        'valid_type': 'string',
        'valid_values': None,
        'default': NO_DEFAULT,
        'description': 'E-mail address for TCOD depositions',
    },
    'warnings.showdeprecations': {
        'key': 'show_deprecations',
        'valid_type': 'bool',
        'valid_values': None,
        'default': True,
        'description': 'Boolean whether to print AiiDA deprecation warnings',
    },
}
