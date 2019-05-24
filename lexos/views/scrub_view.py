import json

from flask import request, session, render_template, Blueprint

from lexos.helpers import constants as constants, \
    general_functions as general_functions
from lexos.managers import utility, session_manager as session_manager

from natsort import humansorted

scrubber_blueprint = Blueprint("scrubber", __name__)


@scrubber_blueprint.route("/scrub", methods=["GET"])
def scrub() -> str:
    """Gets the scrub page.
    :return: The scrub page.
    """

    if "scrubbingoptions" not in session:
        session["scrubbingoptions"] = constants.DEFAULT_SCRUB_OPTIONS
    if "xmlhandlingoptions" not in session:
        session["xmlhandlingoptions"] = {
            "myselect": {"action": "", "attribute": ""}}
    utility.xml_handling_options()

    return render_template("scrub.html")


@scrubber_blueprint.route("/scrub/get-document-previews", methods=["GET"])
def get_document_previews() -> str:
    """Returns previews of the active documents.
    :return: Previews of the active documents.
    """

    file_manager = utility.load_file_manager()
    return json.dumps(file_manager.get_previews_of_active())


@scrubber_blueprint.route("/scrub/download", methods=["GET"])
def download() -> str:
    """Returns a download of the active files.
    :return: the zip files needs to be downloaded.
    """

    file_manager = utility.load_file_manager()
    return file_manager.zip_active_files("scrubbed-documents.zip")


@scrubber_blueprint.route("/scrub/do-scrubbing", methods=["POST"])
def do_scrubbing() -> str:
    """Scrubs the active documents.
    :return: A JSON object with previews of the scrubbed documents.
    """

    file_manager = utility.load_file_manager()

    session_manager.cache_alteration_files()
    session_manager.cache_scrub_options()

    # Save changes only if the "Apply Scrubbing" button is clicked
    saving_changes = request.form["formAction"] == "apply"

    # Scrub
    previews = file_manager.scrub_files(saving_changes=saving_changes)

    # HTML escape the previews
    previews = [[preview[1], general_functions.html_escape(preview[3])]
                for preview in previews]

    # Save the changes if requested
    if saving_changes:
        utility.save_file_manager(file_manager)

    return json.dumps(previews)


@scrubber_blueprint.route("/scrub/get-tag-options", methods=["GET"])
def get_tags_table() -> str:
    """Gets the tags in the active documents.
    :return: The tags in the active documents.
    """

    utility.xml_handling_options()
    tags = humansorted(list(session["xmlhandlingoptions"].keys()))

    response = []
    for tag in tags:
        response.append([tag, session["xmlhandlingoptions"][tag]["action"],
                         session["xmlhandlingoptions"][tag]["attribute"]])

    return json.dumps(response)


@scrubber_blueprint.route("/scrub/save-tag-options", methods=["POST"])
def xml() -> str:
    """Sets the tag options.
    :return: None.
    """

    data = request.json
    utility.xml_handling_options(data)
    return ""


@scrubber_blueprint.route("/scrub/remove-upload", methods=["POST"])
def remove_upload() -> str:
    """Removes a file that was uploaded on the scrubber page.
    :return: None.
    """

    option = request.headers["option"]
    session["scrubbingoptions"]["optuploadnames"][option] = ''
    return ""
