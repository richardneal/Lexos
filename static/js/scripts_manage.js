

/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(document).ready( function () {

/* #### INITIATE MAIN DATATABLE #### */


/* #### END OF TABLE INITIATION #### */	

/* #### DEFINE CONTEXT MENU #### */
	$(document).contextmenu({
		//delegate: 'tr[role="row"]', // Trigger on row
		delegate: 'td', // Trigger on cell
		preventContextMenuForPopup: true,
		preventSelect: true,
		taphold: true,
		// Define menu items
		menu: [
			{title: "Preview Document", cmd: "preview", uiIcon: "ui-icon-search"},
			{title: "Edit Document Label", cmd: "edit-label", uiIcon: "ui-icon-pencil"},
			{title: "Edit Document Class", cmd: "edit-class", uiIcon: "ui-icon-tag"},
			{title: "Delete Document", cmd: "delete", uiIcon: "ui-icon-trash"},
			//{title: "Clone Document", cmd: "clone", uiIcon: "ui-icon-copy"},
			{title: "----"},
			{title: "Select All Documents", cmd: "select-all", uiIcon: "ui-icon-check"},
			{title: "Deselect All Documents", cmd: "deselect-all", uiIcon: "ui-icon-cancel"},
			{title: "----"},
			{title: "Apply Class to Selected Documents", cmd: "apply-class", uiIcon: "ui-icon-tag"},
			{title: "Delete Selected Documents", cmd: "delete-selected", uiIcon: "ui-icon-trash"}
			],
		// Handle menu selection 
		select: function(event, ui) {
			// $target is the element defined in delegate.
			// Variables below assume it is <td>.
			var $target = ui.target;
			var $row = $target.parent();
			var row_id = $row.attr('id');
			var	title = $row.children().eq(1).text();
			// Set function calls for each menu item.
			switch(ui.cmd){
			case "preview":
				showPreviewText(row_id);
				break
			case "edit-label":
				var	cellText = $row.children().eq(1).text();
				editLabel($target, cellText, title, row_id);	
				break
			case "edit-class":
				var	cellText = $row.children().eq(2).text();
				editClass($target, cellText, title, row_id);
				break
			case "delete":
				deleteRow($target, title, row_id);
				break
			case "clone":
				clone($target, title, row_id);
				break
			case "select-all":
				// Activate all documents by ajax.
				selectAll();
				break
			case "deselect-all":
				// De-activate all documents by ajax.
				deselectAll();
				break
			case "apply-class":
				// Apply Class to all selected documents.
				applyClass($target, "");
				break
			case "delete-selected":
				// Delete active files by ajax.
				deleteSelectedRows();
				break
			}
		},
		// Change menu items based on the target.
		beforeOpen: function(event, ui) {
			var $menu = ui.menu,
				$target = ui.target,
				//* Is extraData needed?
				extraData = ui.extraData; // passed when menu was opened by call to open()

			// Enable menu items based on number of selected rows
			var num_selected = enabled.length;
			//* Clone is not enabled at this stage.
			$(document).contextmenu("enableEntry", "clone", false);

			switch (num_selected) {
			// No rows selected
			case 0:
				$(document).contextmenu("enableEntry", "delete-selected", false);
				$(document).contextmenu("enableEntry", "deselect-all", false);
				$(document).contextmenu("enableEntry", "apply-class", false);
				break;
			// 1 row selected
			case 1:
				$(document).contextmenu("enableEntry", "delete-selected", false);
				$(document).contextmenu("enableEntry", "deselect-all", true);
				$(document).contextmenu("enableEntry", "apply-class", false);
				break;
			default:
				$(document).contextmenu("enableEntry", "delete-selected", true);
				$(document).contextmenu("enableEntry", "deselect-all", true);
				$(document).contextmenu("enableEntry", "apply-class", true);				
			}
			// Place the menu on top of the target.
			ui.menu.zIndex($(event.target).zIndex() + 1);
		}
	});
/* #### END OF CONTEXT MENU #### */


/* #### CLICK EVENT HANDLING #### */



/* #### END OF CLICK EVENT HANDLING #### */

/* #### TOOLBAR BUTTON EVENT HANDLING #### */

/*	$("#selectall").click(function() {
		selectAll();
	});

	$("#disableall").click(function() {
		deselectAll();
	});

	$("#delete").click(function() {
		deleteSelectedRows();
	});*/



/* #### END OF TOOLBAR BUTTON EVENT HANDLING #### */
	
});
/* #### END OF $(DOCUMENT).READY() SCRIPTS #### */

/* #### SUPPORTING FUNCTIONS #### */

/* #### toggleId() #### LEGACY FUNCTION: NO LONGER IN USE */
// Toggles the document state by Ajax, then toggles the UI selected state for the item.
function toggleId(id) {
	row_id = "#" + id;
	$.ajax({
		type: "POST",
		url: document.URL,
		data: id.toString(),
		contentType: 'charset=UTF-8',
		headers: { 'toggleFile': 'dummy' },
		beforeSend: function(){
     		$("#status").show();
   		},
		//success: function() {
		//},
		complete: function(){
     		$("#status").hide();
   		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Your action could not be saved to the session file.')
			$("#"+id).removeClass("ui-selected");
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	});
}
/* #### END OF toggleId() #### */

/* #### editLabel() #### */
// Opens a JQuery UI dialog to edit a document label. On submit, the File Manager is updated by Ajax.
function editLabel($target, cellText, title, row_id) {
	var form = 'Document Label <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: row_id.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'setLabel': unescape(encodeURIComponent(val.toString())) },
				success: function(response) {
					$target.text(val);
					$("#editLabel").dialog("close");
					$("#editLabel").remove();
					tr = $target.parent();
					table.row(tr).invalidate().draw();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editLabel" title="Document Label for ' + title + '">' + form + '</div>').dialog(opts);
}
/* #### END OF editLabel() #### */

/* #### editClass() #### */
// Opens a JQuery UI dialog to edit a document class. On submit, the File Manager is updated by Ajax.
function editClass($target, cellText, title, row_id) {
	var form = 'Class Prefix <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: row_id.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'setClass': unescape(encodeURIComponent(val.toString())) },
				success: function(response) {
					console.log("Success: "+response);
					$target.text(val);
					tr = $target.parent();
					table.row(tr).invalidate().draw();
					$("#editClass").dialog("close");
					$("#editClass").remove();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editClass" title="Add Class Prefix to ' + title + '">' + form + '</div>').dialog(opts);
}
/* #### END OF editClass() #### */

/* #### applyClass() #### */
// Opens a JQuery UI dialog to edit a document class. On submit, all selected documents are updated in the File Manager by Ajax.
function applyClass($target, cellText) {
	var form = 'Class Prefix <input id="tmp" type="text" value="'+cellText+'">';
	var opts = {
		height:200,
		width:400,
		buttons: {
		"Save": function() {
			val = $("#tmp").val();
			// Send by ajax, update table, and close on success
			$.ajax({
				type: "POST",
				url: document.URL,
				data: val.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'applyClassLabel': 'dummy' },
				success: function(response) {
					$('.class-label').each(function() {
						if ($(this).parent().hasClass("selected")) {
							$(this).html(val);
						}
					});
					tr = $target.parent();
					table.row(tr).invalidate().draw();
					$("#editClass").dialog("close");
					$("#editClass").remove();
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert('Error: Your action could not be saved to the session file.')
				$("#"+id).removeClass("ui-selected");
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		},
		"Cancel": function() {
			$(this).dialog("close");		
		}}
	};
	$('<div id="editClass" title="Apply Class Prefix to All Selected Files">' + form + '</div>').dialog(opts);
}
/* #### END OF applyClass() #### */

/* #### showPreviewText() #### */
//* Opens a JQuery UI dialog containing the document preview text. Eventually, this should be replaced with the complete text in an editor.
function showPreviewText(row_id) {
	$.ajax({
		type: "POST",
		url: document.URL,
		data: row_id,
		contentType: 'charset=UTF-8',
		headers: { 'previewTest': 'dummy' },
		success: function(response) {
			response = JSON.parse(response);
			console.log(response);
			title = response["label"];
			text = response["previewText"];
			// Encode tags as HTML entities
			text = String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
			//* To Do: Convert tagged texts to strings
			$('<div id="preview" title="Preview of ' + title + '">' + text + '</div>').dialog({height:500,width:500});
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Lexos could not retrieve the file preview.');
			// display error if one
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	});
}
/* #### END OF showPreviewText() #### */

/* #### selectAll() #### */
// Sets the selected status of all documents in the File Manager and UI to selected.
function selectAll() {
	$.ajax({
		type: "POST",
		url: document.URL,
		data: 'dummy',
		headers: { 'selectAll': 'dummy' },
		success: function() {
			$("#demo tbody tr").addClass("ui-selected");
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Lexos could not perform the requested function.')
			// display error if one
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	}).then(function(){
		location.reload();
	});
}
/* #### END OF selectAll() #### */

/* #### deselectAll() #### */
// Removes the selected status of all documents in the File Manager and UI.
function deselectAll() {
	$.ajax({
		type: "POST",
		url: document.URL,
		data: 'dummy',
		headers: { 'disableAll': 'dummy' },
		success: function() {
			$("#demo tbody tr").removeClass("ui-selected");
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('Error: Lexos could not perform the requested function.')
			// display error if one
			console.log("bad: " + textStatus + ": " + errorThrown);
		}
	}).then(function(){
		location.reload();
	});
}
/* #### END OF deselectAll() #### */

/* #### deleteRow() #### */
// Deletes a single document in the File Manager and UI.
function deleteRow(target, title, row_id) {
	// Center the caution prompt in the window.
	$('#delete-confirm-wrapper').center();
	$('#delete-explanation').html("Are you sure you want to delete "+title+"?");
	$('#delete-confirm-wrapper').addClass("showing");
	// If the user clicks the cancel button, close the dialog.
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// If the user clicks confirm, delete the selection.
	$('#confirm-delete-bttn').click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: row_id,
			headers: { 'deleteRow': 'dummy' },
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				target.parent().remove();
			},
			error: function(jqXHR, textStatus, errorThrown){
				alert('Error: Lexos could save your changes to the session file.')
				console.log(errorThrown);
			}
		});
	});
}

/* #### END OF deleteRow() #### */

/* #### deleteSelectedRows() #### */
// Deletes selected documents in the File Manager and UI.
function deleteSelectedRows() {
	// Center the caution prompt in the window.
	$('#delete-confirm-wrapper').center();
	$('#delete-confirm-wrapper').addClass("showing");
	// If the user clicks the cancel button, close the dialog.
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// If the user clicks confirm, delete the selected documents.
	$('#confirm-delete-bttn').click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: "",
			headers: { 'deleteActive': 'dummy' },
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				$("#demo tbody tr").each(function() {
					if ($(this).hasClass("ui-selected")) {
						$(this).remove();
					}
				});
				console.log(enabled);
			},
			error: function(jqXHR, textStatus, errorThrown){
				alert('Error: Lexos could save your changes to the session file.')
				console.log(errorThrown);
			}
		}).then(function(){
			location.reload();
		});
	});

}

/* #### END OF deleteSelectedRows() #### */

/* Functions called in lexos.py */
//Javascript         -->    Ajax Call*
//------------------------------------------
//toggleFile         -->    toggleFile
//editLabel          -->    setLabel
//editClass          -->    setClass
//applyClass         -->    applyClassLabel
//showPreviewText    -->    previewTest
//selectAll          -->    selectAll
//deselectAll        -->    disableAll
//deleteRow          -->    deleteRow
//deleteSelectedRows -->    deleteActive

// * Calls are made through select2() in the 
// Development Section of lexos.py.
// ** Missing function.

// By default, select2() calls getPreviewsOfAll()*.
// Otherwise, the following functions are called:
// lexos.py        -->    ModelClasses.py
// -------------------------------------------
// previewTest     -->    getPreview
// toggleFile      -->    toggleFile
// setLabel        -->    Handled in lexos.py
// setLabel        -->    Handled in lexos.py and setName 
// setClass        -->    Handled in lexos.py and
//                          setClassLabel
// selectAll       -->    enableAll
// applyClassLabel -->    classifyActiveFiles
// deleteActive    -->    deleteActiveFiles
// deleteRow       -->    deleteOneFile*

// *In the development section.
// ** Development section has classifyFile, which is not used.