///////////////////////////////////////////////
//API calls
///////////////////////////////////////////////
function markAsReady(job_id, dt) {
    jQuery.get(
        host + '/set_job_status/' + job_id + '/' + dt + '/ready',
        function(data) {
           alert('restarted ' + job_id + ' ' + dt );
           window.location.reload();
        }
    );
};

function markAsFailed(job_id, dt) {
    $.get(
        host + '/set_job_status/' + job_id + '/' + dt + '/failed',
        function(data) {
           alert('marked as failed ' + job_id + ' ' + dt );
           window.location.reload();
        }
    );
};

function markAsSucceeded(job_id, dt) {
    jQuery.get(
        host + '/set_job_status/' + job_id + '/' + dt + '/succeeded',
        function(data) {
           alert('marked as failed ' + job_id + ' ' + dt );
           window.location.reload();
        }
    );
};

function markAsNotReady(job_id, dt) {
    jQuery.get(
        host + '/set_job_status/' + job_id + '/' + dt + '/not_ready',
        function(data) {
           alert('marked as failed ' + job_id + ' ' + dt );
           window.location.reload();
        }
    );
};

///////////////////////////////////////////////
//Data transformations
///////////////////////////////////////////////

//Returns a sorted list of unique schedule_time strings from http://<drone-web>/list_jobs response object
function sortedScheduleTimeList(jsonObject) {
    var len = jsonObject.length;
    var schedule_time_list = [];


    for ( i=0; i < len; i+=1 ) {

        if ($.inArray(jsonObject[i].schedule_time, schedule_time_list) == -1) {
            schedule_time_list.push(jsonObject[i].schedule_time);
        }
    }
    return schedule_time_list.sort();
};

//Returns a aoColumns object
function getColumns(jsonObject) {

    var uniqueScheduleDates = sortedScheduleTimeList(jsonObject);
    var len = uniqueScheduleDates.length;

    var cols = [{ "mData": "job_id"}]

    for ( i=0; i < len; i+=1 ) {
            cols.push({ "mData": uniqueScheduleDates[i]});
    }

    return cols;
};

//Returns a aoColumnDefs object
function getColumnDefinitions(jsonObject) {
    var colDef = [{aTargets: [0], sTitle: "Name", bSearchable: 'true'}];

    var uniqueScheduleDates = sortedScheduleTimeList(jsonObject);
    var len = uniqueScheduleDates.length;

    for ( i=0; i < len; i+=1 ) {
            colDef.push({aTargets: [i+1], sTitle: uniqueScheduleDates[i].replace('T', ' ')});
    }

    return colDef;
};

//Returns a map {job_id: {schedule_time: <arg>}} from http://<drone-web>/list_jobs response object
function getJobScheduleKeyObject(jsonObject, keyName) {

    var len = jsonObject.length;
    var result = {};

    var createNestedObject = function( base, names ) {
        for( var i = 0; i < names.length; i++ ) {
            base = base[ names[i] ] = base[ names[i] ] || {};
        }
    };

    for ( i=0; i < len; i+=1 ) {
        var scheduleTime = jsonObject[i].schedule_time;
        var value = jsonObject[i][keyName];
        createNestedObject(result, [jsonObject[i].job_id, scheduleTime]);
        result[jsonObject[i].job_id][scheduleTime] = value;
    }

    return result;
};

//Returns a map {job_id: [{schedule_time: <arg>}, ...]} from http://<drone-web>/list_jobs response object
function getJobScheduleKeyArrayObject(jsonObject, keyName) {
    var len = jsonObject.length;
    var jobScheduleStatusMap = {};

    for ( i=0; i < len; i+=1 ) {
        var jobId = jsonObject[i].job_id;
        var scheduleTime = jsonObject[i].schedule_time;
        var status = jsonObject[i].status;

        if (jobScheduleStatusMap.hasOwnProperty(jobId)) {
            jobScheduleStatusMap[jobId].push(JSON.parse('{"' + scheduleTime + '":"' + status + '"}'));
        } else {
            jobScheduleStatusMap[jobId] = [JSON.parse('{"' + scheduleTime + '":"' + status + '"}')];
        }
    }
    return jobScheduleStatusMap
};

//Converts YYYY-mm-ddTHH:MM:SS to sYYYY-mm-ddTHH-MM-SS
function encodeDate(string) {
    var find = ':';
    var re = new RegExp(find,'g');
    var encoded_string = 's' + string.replace(re, '-');
    return encoded_string;
}

//Converts sYYYY-mm-ddTHH-MM-SS to YYYY-mm-ddTHH:MM:SS
function decodeDate(string) {
    var date_time_split = string.split('T');
    var dateString = date_time_split[0].replace('s', '');
    var timeString = date_time_split[1];

    var find = '-';
    var re = new RegExp(find,'g');
    var decodedTimeString = timeString.replace(re, ':');

    return dateString + 'T' + decodedTimeString;
}

//Generate a dropdown list with options
function getDropDownOptions(job_id, schedule_time) {
    var option1 = '<input type="button" class="alert button dropdown" value="ready" onClick=markAsReady("' + job_id + '","' + schedule_time + '")>';
    var option2 = '<input type="button" class="alert button dropdown" value="not_ready" onClick=markAsNotReady("' + job_id + '","' + schedule_time + '")>';
    var option3 = '<input type="button" class="alert button dropdown" value="failed" onClick=markAsFailed("' + job_id + '","' + schedule_time + '")>';
    var option4 = '<input type="button" class="alert button dropdown" value="succeeded" onClick=markAsSucceeded("' + job_id + '","' + schedule_time + '")>';
    return option1 + option2 + option3 + option4;
}

//Map a button type to a job status
function getButtonType(status) {
    if (status == 'succeeded') {
            return "success button dropdown tiny";
        } else if (status == 'failed') {
            return "alert button dropdown tiny";
        } else if (status == 'not_ready') {
            return "secondary button dropdown tiny";
        } else if (status == 'running') {
            return "button dropdown tiny";
        } else if (status == 'ready') {
            return "button dropdown tiny";
        } else {
            return "disabled button"
        }
}

//Returns a aaData object from http://<drone-web>/list_jobs response object
function getJobInfo(jsonObject) {

    var len = jsonObject.length;
    var jobRuns = getJobScheduleKeyObject(jsonObject, "runs");
    var jobScheduleStatusMap = getJobScheduleKeyArrayObject(jsonObject, 'status');
    var results = [];

    for ( property in jobScheduleStatusMap ) {

        var temp = {job_id: property};
        var jobLen = jobScheduleStatusMap[property].length;
        var job_id = property;

        for ( i=0; i < jobLen; i+=1 ) {
            var t = Object.keys(jobScheduleStatusMap[property][i]).map(function (key) {return [key, jobScheduleStatusMap[property][i][key]]});
            var status = t[0][1];
            var schedule_time = t[0][0]
            var dropdownOptions = getDropDownOptions(job_id, schedule_time);
            var unique_job_id = job_id + '_' + encodeDate(schedule_time);
            var runs = jobRuns[job_id][schedule_time];

            var buttonHTML = '<div class="button-bar"' + '><button href="#" data-dropdown="drop_' +
                        unique_job_id +
                        '" aria-controls="drop_' +
                        unique_job_id +
                        '" aria-expanded="false" class="' + getButtonType(status) + '">' +
                        runs +
                        '</button>' +
                        '<ul id="drop_' + unique_job_id + '" data-dropdown-content class="f-dropdown" aria-hidden="true">' +
                        dropdownOptions + '</ul></div>'

            temp[schedule_time] = buttonHTML;
        }

        results.push(temp);
    }

    return results;

};