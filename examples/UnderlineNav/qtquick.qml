import QtQuick
import Purrimer

UnderlineNav {
    width: 488
    items: [
        { label: "Code", icon: "code" },
        { label: "Issues", icon: "issue-opened", count: 12 },
        { label: "Pull requests", icon: "git-pull-request", count: 3 },
        { label: "Actions", icon: "play" }
    ]
    onSelected: (index) => console.log("page", index)
}
