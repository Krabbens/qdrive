import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

ApplicationWindow {
    id: applicationWindow
    flags: Qt.Window
    visible: true
    width: 1200
    height: 800
    title: qsTr("template")
    Material.theme: Material.Dark
    Pane {
        padding: 0
        anchors.fill: parent
        background: Rectangle {
                anchors.fill: parent
                color:"#202020"
            }
        Text {
            anchors.centerIn: parent
            text: "text"
            color: "#ffffff"
        }
    }
}