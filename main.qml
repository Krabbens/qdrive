import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import "Components"

ApplicationWindow {
    id: app
    flags: Qt.Window
    visible: true
    width: 1200
    height: 800
    title: qsTr("template")

    property var bgColor: "#212429"
    property var fgColor: "#f0eff0"
    property var primaryColor: "#30333a"
    property var secondaryColor: "#212429"
    property var accentColor: "#2785fa"
    property var textColor: "#ffffff"

    FontLoader { id: poppins_reg; source: "./Source/Fonts/Poppins-Regular.ttf" }
    FontLoader { id: poppins_med; source: "./Source/Fonts/Poppins-Medium.ttf" }
    FontLoader { id: poppins_semibold; source: "./Source/Fonts/Poppins-SemiBold.ttf" }
    FontLoader { id: poppins_bold; source: "./Source/Fonts/Poppins-Bold.ttf" }
    FontLoader { id: fontawesome; source: "./Source/Fonts/fontawesome-solid.otf" }

    Rectangle {
        anchors.fill: parent
        color: app.bgColor
    }

    Material.theme: Material.Dark
    Pane {
        padding: 0
        anchors.fill: parent
        background: Rectangle {
                anchors.fill: parent
                color: app.bgColor
            }
        Pane {
            padding: 0
            id: logoHeader
            width: parent.width
            height: 80
            anchors.top: parent.top
            anchors.left: parent.left
            Rectangle {
                anchors.fill: parent
                color: app.bgColor
            }
            Rectangle {
                // horizontal line spacer
                width: parent.width
                height: 1
                color: "#bcbdbe"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
            }
            Text {
                id: appIcon
                text: "\ue185"
                color: app.textColor
                font.pixelSize: 30
                font.family: fontawesome.name
                anchors.left: parent.left
                anchors.leftMargin: 50  
                anchors.verticalCenter: parent.verticalCenter

            }
            Text {
                id: appName
                text: "qdrive"
                color: app.textColor
                font.pixelSize: 30
                font.family: poppins_bold.name
                font.weight: Font.Medium
                anchors.left: appIcon.right
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 5
            }
        }
        Pane {
            padding: 0
            id: mainContent
            width: parent.width
            height: parent.height - logoHeader.height
            anchors.top: logoHeader.bottom
            anchors.left: parent.left

            Rectangle {
                anchors.fill: parent
                color: app.bgColor
            }
            Text {
                id: title
                text: "All Files"
                color: app.textColor
                font.pixelSize: 30
                font.family: poppins_bold.name
                font.weight: Font.Medium
                anchors.left: parent.left
                anchors.leftMargin: 50 
                anchors.top: parent.top
                anchors.topMargin: 20
            }
            ListView {
                id: list
                anchors.top: title.bottom
                anchors.left: parent.left
                anchors.leftMargin: 20
                width: parent.width - 40
                height: parent.height - 40
                model: fileList
                spacing: 0
                delegate: ItemDelegate {
                    width: parent.width - 40
                    height: 60
                    contentItem: ListDelegate {
                        width: parent.width
                        height: parent.height
                        id: fileButton
                        text: model.name
                        font.pixelSize: 20
                        font.family: poppins_med.name
                        primaryColor: app.bgColor
                        secondaryColor: app.primaryColor
                        icon: model.icon
                        date: model.date
                        callback: function() {
                            console.log("clicked")
                        }
                    }
                    background: Rectangle {
                        anchors.fill: parent
                        color: app.bgColor
                    }
                }
            }

            Spinner {
                id: fileListLoader
                anchors.centerIn: list
                width: 100
                height: 100
                running: false
            }
        }
    }
}

// --text: #f0eff0;
// --background: #0b0a0a;
// --primary: #383337;
// --secondary: #282527;
// --accent: #91888f;
