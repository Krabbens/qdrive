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

        Rectangle {
            id: bg
            width: 200
            height: 50
            anchors.centerIn: parent
            color: "#3b82f6"
            radius: 5

            ColorAnimation on color {
                running: ma.hovered
                duration: 200
                from: bg.color
                to: "#3b82f6"
            }

            ColorAnimation on color {
                running: !ma.hovered
                duration: 200
                from: bg.color
                to: "#2563eb"
            }

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
                anchors.fill: parent
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
            horizontalOffset: 1
            verticalOffset: 2
            radius: 7.0
            samples: 17
            color: "#1A000000"
            source: bg
        }
    }
}