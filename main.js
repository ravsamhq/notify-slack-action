/* jshint node: true */
/* jshint esversion: 6 */
/* jshint strict:false */
const https = require("https");

// Get an action colour based on workflow status
function actionColor(status) {
    switch(status) {
        case "success":
            return "good";
        case "failure":
            return "danger";
        default:
            return "warning";
    }
}
// Get a transformed status based on workflow status
function actionStatus(status) {
    switch(status) {
        case "success":
            return "passed";
        case "failure":
            return "failed";
        default:
            return "passed with warnings";
    }
}

// Get an emoji based on workflow status
function actionEmoji(status, icon_success, icon_failure, icon_warnings) {
    switch(status) {
        case "success":
            return icon_success;
        case "failure":
            return icon_failure;
        default:
            return icon_warnings;
    }
}

// Creates a message payload which can be sent to Slack
function constructPayload(inputs, callback) {
    // derived from workflow environment
    const workflow = process.env.GITHUB_WORKFLOW;
    const repo = process.env.GITHUB_REPOSITORY;
    const branch = process.env.GITHUB_REF_NAME;
    const commit_sha = process.env.GITHUB_SHA.substring(0, 7);
    const run_id = process.env.GITHUB_RUN_ID;
    const job = process.env.GITHUB_JOB;

    // derived from action inputs
    const job_status = inputs.job_status;
    let message = inputs.message_format;
    let title = inputs.notification_title;
    let footer = inputs.footer;
    const mention_users = inputs.mention_users;
    const mention_users_when = inputs.mention_users_when;
    const mention_groups = inputs.mention_groups;
    const mention_groups_when = inputs.mention_groups_when;
    const icon_success = inputs.icon_success;
    const icon_failure = inputs.icon_failure;
    const icon_warnings = inputs.icon_warnings;

    // self constructed
    const patterns = {
        repo: repo,
        branch: branch,
        commit_sha: commit_sha,
        commit_url: `https://github.com/${repo}/commit/${commit_sha}`,
        repo_url: `https://github.com/${repo}`,
        run_url: `https://github.com/${repo}/actions/runs/${run_id}`,
        job: job,
        workflow: workflow,
        color: actionColor(job_status),
        status_message: actionStatus(job_status),
        emoji: actionEmoji(job_status, icon_success, icon_failure, icon_warnings),
    };

    // construct title
    for (const pattern in patterns) {
        title = title.replaceAll(`{${pattern}}`, patterns[pattern]);
    }

    // construct message
    for (const pattern in patterns) {
        message = message.replaceAll(`{${pattern}}`, patterns[pattern]);
    }

    // add user mentions
    if (mention_users_when.includes(job_status) && mention_users.trim() !== "") {
        message += "\n";
        const users = mention_users.split(",");
        for (let i = 0; i < users.length - 1; i++) {
            message = message + `<"${users[i]}>`;
        }
    }

    // add group mentions
    if (mention_groups_when.includes(job_status) && mention_groups.trim() !== "") {
        message += "\n";
        const groups = mention_groups.split(",");
        for (let i = 0; i < groups.length - 1; i++) {
            if (groups[i].trim().charAt(0) === "!") {
                message = message + `<${groups[i]}>`;
            } else {
                message = message + `<!subteam^${groups[i]}>`;
            }
        }
    }

    // construct footer
    for (const pattern in patterns) {
        footer = footer.replaceAll(`{${pattern}}`, patterns[pattern]);
    }

    const payload = {
        "attachments": [
            {
                "text": message,
                "fallback": title,
                "color": patterns.color,
                "mrkdwn_in": ["text"],
                "footer": footer,
            }
        ]
    };

    callback(JSON.stringify(payload));
}

// Send a Slack notification
function notifySlack(payload) {
    console.log("Sending message to Slack...");
    const url = new URL(process.env.SLACK_WEBHOOK_URL);
    const options = {
        hostname: url.hostname,
        port: 443,
        path: url.pathname,
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(payload, 'utf8'),
        },
        agent: new https.Agent({ keepAlive: false }),
    };
    const req = https.request(options, resp => {
        // Receive data from the request
        let data = "";
        resp.on("data", chunk => {
            data += chunk;
        });
        // Handle response once it's been fully received
        resp.on("end", () => {
            console.log("Response body:", data);
            if (resp.statusCode === 200) {
                console.log("Sent message to Slack OK");
            } else {
                console.error("Payload:", payload);
                throw Error(`Failed to post to Slack! statusCode = ${resp.statusCode}`);
            }
        });
    }).on("error", (err) => {
        console.error("Payload:", payload);
        console.error("Error making request to Slack:", err);
        throw Error("Failed to make request to Slack");
    });
    req.write(payload);
    req.end();
}


function main() {
    const inputs = {
        job_status: process.env.INPUT_STATUS,
        notification_title: process.env.INPUT_NOTIFICATION_TITLE,
        message_format: process.env.INPUT_MESSAGE_FORMAT,
        footer: process.env.INPUT_FOOTER,
        notify_when: process.env.INPUT_NOTIFY_WHEN,
        mention_users: process.env.INPUT_MENTION_USERS,
        mention_users_when: process.env.INPUT_MENTION_USERS_WHEN,
        mention_groups: process.env.INPUT_MENTION_GROUPS,
        mention_groups_when: process.env.INPUT_MENTION_GROUPS_WHEN,
        icon_success: process.env.INPUT_ICON_SUCCESS,
        icon_failure: process.env.INPUT_ICON_FAILURE,
        icon_warnings: process.env.INPUT_ICON_WARNINGS,
    };

    constructPayload(inputs, (payload) => {
        if (inputs.notify_when.includes(inputs.job_status)) {
            notifySlack(payload);
        }
    });
}

if (require.main === module) {
    main();
}
