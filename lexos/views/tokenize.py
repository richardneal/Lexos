import json

from flask import session, render_template, send_file, Blueprint

from lexos.managers import session_manager
from lexos.helpers import constants as constants
from lexos.models.tokenizer_model import TokenizerModel

tokenize_blueprint = Blueprint("tokenize", __name__)


@tokenize_blueprint.route("/tokenize", methods=["GET"])
def tokenizer():
    """Handles the functionality on the tokenizer page.
    :return: The tokenize page.
    """

    # Set the default session options.
    session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Send the page.
    return render_template("tokenize.html")


@tokenize_blueprint.route("/tokenize/table", methods=["POST"])
def get_table():
    """Gets the requested table data.
    :return: The requested table data.
    """

    # Cache the options.
    session_manager.cache_analysis_option()

    # Return the generated document term matrix.
    return json.dumps(TokenizerModel().get_table())


@tokenize_blueprint.route("/tokenize/csv", methods=["POST"])
def download():
    """Gets the table data in a CSV.
    :return: The table data in a CSV.
    """

    # Cache the options.
    session_manager.cache_analysis_option()

    # Return the table data CSV
    return TokenizerModel().get_csv()