import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12
import QtQuick.Controls.Material.impl 2.12

Item {
    FontLoader { id: fontawesome; source: "../Source/Fonts/fontawesome-solid.otf" }
    FontLoader { id: poppins_reg; source: "../Source/Fonts/Poppins-Regular.ttf" }
    property alias text: textItem.text
    property alias textColor: textItem.color
    property alias fontSize: textItem.font.pixelSize
    property alias font: textItem.font
    property alias icon: icon.text
    property alias date: date.text
    property alias size: size.text

    property var id

    property var primaryColor
    property var secondaryColor

    property var callback
    property var callbackDbl

    property var secondaryTextColor: "#a7a7aa"
    
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
            clip: true

            ColorAnimation on color {
                running: ma.hovered
                duration: 300
                from: primaryColor
                to: secondaryColor
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: !ma.hovered
                duration: 300
                from: secondaryColor
                to: primaryColor
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: ma.pressed
                duration: 100
                from: secondaryColor
                to: Qt.lighter(secondaryColor, 1.2)
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: !ma.pressed
                duration: 100
                from: Qt.lighter(secondaryColor, 1.2)
                to: secondaryColor
                easing.type: Easing.InOutQuad
            }

            Text {
                id: icon
                anchors.left: checkBox.right
                anchors.leftMargin: text == "\uf07b" || "\uf0e2"  ? 7 : 10
                anchors.verticalCenter: parent.verticalCenter
                text: ""
                color: "#FFFFFF"
                font.pixelSize: 20
                font.family: fontawesome.name
            }

            Text {
                id: textItem
                anchors.left: checkBox.right
                anchors.leftMargin: 40
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 2
                text: ""
                color: "#FFFFFF"
                font.pixelSize: 20
                font.family: poppins_reg.name
            }

            Text {
                id: date
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 2
                text: ""
                color: secondaryTextColor
                font.pixelSize: 18
                font.family: poppins_reg.name
            }

            Text {
                id: size
                anchors.right: parent.right
                anchors.rightMargin: parent.width * 0.17
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 2
                text: ""
                visible: type == "file"
                color: secondaryTextColor
                font.pixelSize: 18
                font.family: poppins_reg.name
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
                onDoubleClicked: {
                    if (callbackDbl) {
                        callbackDbl(textItem.text)
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

            CheckBox {
                id: checkBox
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                checked: false
                Material.accent: "#4587de"
            }
        }
        DropShadow {
            anchors.fill: bg
            horizontalOffset: 0
            verticalOffset: 10
            radius: 50.0
            samples: 100
            color: "#44" + secondaryColor.replace("#", "")
            source: bg

            ColorAnimation on color {
                running: !ma.hovered
                duration: 300
                from: "#44" + secondaryColor.replace("#", "")
                to: "#00" + secondaryColor.replace("#", "")
                easing.type: Easing.InOutQuad
            }

            ColorAnimation on color {
                running: ma.hovered
                duration: 300
                from: "#00" + secondaryColor.replace("#", "")
                to: "#44" + secondaryColor.replace("#", "")
                easing.type: Easing.InOutQuad
            }
        }
    }
}