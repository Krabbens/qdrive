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

    property var callback
    
    Item {
        id: item
        width: 300
        height: 100
        anchors.horizontalCenter: parent.horizontalCenter
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
            width: 200
            height: 50
            anchors.centerIn: parent
            color: "#383337"
            radius: 5
            border.width: 1
            border.color: "#4f4b4f"

            Text {
                id: textItem
                anchors.centerIn: parent
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
                    console.log("Clicked")
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
            samples: 30
            color: "#BB383337"
            source: bg

            ColorAnimation on color {
                running: !ma.hovered
                duration: 300
                from: "#BB383337"
                to: "#00383337"
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: ma.hovered
                duration: 300
                from: "#00383337"
                to: "#BB383337"
                easing.type: Easing.InOutQuad
            }
        }
    }
}