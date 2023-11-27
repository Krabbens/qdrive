import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.3
import "Components"

ApplicationWindow {
    id: app
    flags: Qt.Window | Qt.FramelessWindowHint
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
            border.color: "#FFFFFF"
            border.width: 1
        }
        Pane {
            padding: 0
            id: logoHeader
            width: parent.width
            height: 50
            anchors.top: parent.top
            anchors.left: parent.left
            Rectangle {
                anchors.fill: parent
                color: app.bgColor
            }
            Pane {
                id: titlebarButtons
                width: 100
                height: 50
                anchors.top: parent.top
                anchors.right: parent.right
                padding: 0
                Rectangle {
                    width: 50
                    height: 50
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    color: app.bgColor
                    Text {
                        text: "✕"
                        color: "#EEEEEE"
                        font.pointSize: 18
                        anchors.centerIn: parent
                    }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onPressedChanged: parent.opacity = containsPress ? 0.7 : 1
                        onReleased: callback.exit()
                        onHoveredChanged: parent.color = containsMouse ? "#FF2828" : app.bgColor
                    }
                }
                Rectangle {
                    width: 50
                    height: 50
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    color: app.bgColor
                    Text{
                        text: "−"
                        color: app.textColor
                        font.pointSize: 18
                        anchors.centerIn: parent
                    }
                    MouseArea{
                        anchors.fill: parent
                        hoverEnabled: true
                        onPressedChanged: parent.opacity = containsPress ? 0.7 : 1
                        onReleased: callback.minimize()
                        onHoveredChanged: parent.color = containsMouse ? "#373737" : app.bgColor
                    }
                }
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
                font.pixelSize: 23
                font.family: fontawesome.name
                anchors.left: parent.left
                anchors.leftMargin: 50  
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                id: appName
                text: "qdrive"
                color: app.textColor
                font.pixelSize: 23
                font.family: poppins_bold.name
                font.weight: Font.Medium
                anchors.left: appIcon.right
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 3
            }
            MouseArea {
                height: parent.height
                width: parent.width - 100
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.verticalCenter: parent.verticalCenter
                property var lastmousex: 0
                property var lastmousey: 0
                onPressed: {
                    lastmousex = mouseX;
                    lastmousey = mouseY;
                }
                onMouseXChanged: app.x += (mouseX - lastmousex)
                onMouseYChanged: app.y += (mouseY - lastmousey)
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
                property var currentFile
                id: list
                anchors.top: title.bottom
                anchors.left: parent.left
                anchors.leftMargin: 20
                width: parent.width - 40
                height: parent.height - 40
                model: fileList
                spacing: 0
                delegate: ItemDelegate {
                    width: parent ? parent.width - 40 : 0
                    height: 60
                    contentItem: ListDelegate {
                        width: parent.width
                        height: parent.height
                        id: fileButton
                        vindex: index
                        text: model.name
                        font.pixelSize: 20
                        font.family: poppins_med.name
                        primaryColor: app.bgColor
                        secondaryColor: app.primaryColor
                        icon: model.icon
                        date: model.date
                        size: model.size
                        vmodel: model
                        callbackDbl: model.type === "directory" ? open_directory_async : download_file_async
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
                running: true
                visible: false
            }
        }
        Rectangle {
            id: leftBorder
            width: 1
            height: parent.height
            color: app.primaryColor
            anchors.left: parent.left
            anchors.leftMargin: 0
        }
        Rectangle {
            id: rightBorder
            width: 1
            height: parent.height
            color: app.primaryColor
            anchors.right: parent.right
            anchors.rightMargin: 0
        }
        Rectangle {
            id: topBorder
            width: parent.width
            height: 1
            color: app.primaryColor
            anchors.top: parent.top
            anchors.topMargin: 0
        }
        Rectangle {
            id: bottomBorder
            width: parent.width
            height: 1
            color: app.primaryColor
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
        }
    }

    function toggleLoader() {
        fileListLoader.visible = !fileListLoader.visible
    }

    function setCurrentDirectoryText(dir) {
        if (dir === "/") {
            title.text = "All Files"
        } else {
            title.text = dir
        }
    }

    function open_directory_async(model) {
        callback.open_directory_async(model.name)
    }

    function download_file_async(index) {
        //list.currentFile = index
        callback.download_file_async(index)
    }
}

// --text: #f0eff0;
// --background: #0b0a0a;
// --primary: #383337;
// --secondary: #282527;
// --accent: #91888f;
