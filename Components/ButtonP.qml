import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

Item {
    property alias text: textItem.text
    property alias textColor: textItem.color
    property alias fontSize: textItem.font.pixelSize
    property alias font: textItem.font

    property var primaryColor
    property var secondaryColor

    property var callback
    
    Item {
        id: item
        width: parent.width
        height: parent.height
        anchors.left: parent.left
        anchors.top: parent.top

        NumberAnimation on anchors.topMargin {
            running: ma.hovered
            duration: 200
            from: 0
            to: -5
        }

        NumberAnimation on anchors.topMargin {
            running: !ma.hovered
            duration: 200
            from: -5
            to: 0
        }

        Rectangle {
            id: bg
            width: parent.width
            height: parent.height
            anchors.centerIn: parent
            color: primaryColor
            radius: 5
            border.width: 1
            border.color: secondaryColor

            Text {
                id: textItem
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 2
                text: ""
                color: "#FFFFFF"
                font.pixelSize: 20
            }

            MouseArea {
                id: ma
                property bool hovered: false
                hoverEnabled: true
                width: parent.width
                height: parent.height + 5
                anchors.top: parent.top
                anchors.left: parent.left
                NumberAnimation on anchors.topMargin {
                    running: ma.hovered
                    duration: 200
                    from: 0
                    to: 5
                }

                NumberAnimation on anchors.topMargin {
                    running: !ma.hovered
                    duration: 200
                    from: 5
                    to: 0
                }
                onClicked: {
                    if (callback) {
                        callback()
                    }
                }
                onEntered: {
                    hovered = true
                    cursorShape = Qt.PointingHandCursor
                }
                onExited: {
                    hovered = false
                    cursorShape = Qt.ArrowCursor
                }
            }
        }
        DropShadow {
            anchors.fill: bg
            horizontalOffset: 0
            verticalOffset: 10
            radius: 50.0
            samples: 100
            color: "#BB" + primaryColor.replace("#", "")
            source: bg

            ColorAnimation on color {
                running: !ma.hovered
                duration: 300
                from: "#BB" + primaryColor.replace("#", "")
                to: "#00" + primaryColor.replace("#", "")
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: ma.hovered
                duration: 300
                from: "#00" + primaryColor.replace("#", "")
                to: "#BB" + primaryColor.replace("#", "")
                easing.type: Easing.InOutQuad
            }
        }
    }
}