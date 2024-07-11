# MIT License

# Copyright (c) 2022 CS Goh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
from .event import *
from .activity import *
from .gateway import *
from .helper import Helper
from .version import __version__


@dataclass
class BPMN:
    """BPMN diagram"""

    id: str = field(init=False)
    name: str = field(init=False)

    _pools: list = field(init=False, default_factory=list)

    # *** Create the root element ***
    definitions = ET.Element(
        "bpmn:definitions",
        {
            "id": f"Definitions_{Helper.get_uuid()}",
            "targetNamespace": "https://github.com/csgoh/processpiper/schema/bpmn",
            "exporter": "ProcessPiper (https://github.com/csgoh/processpiper)",
            "exporterVersion": __version__,
            "xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
            "xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
            "xmlns:di": "http://www.omg.org/spec/DD/20100524/DI",
            "xmlns:bioc": "http://bpmn.io/schema/bpmn/biocolor/1.0",
            "xmlns:color": "http://www.omg.org/spec/BPMN/non-normative/color/1.0",
        },
    )

    def render_sample(self, pools, filename):
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)

        collaboration = ET.SubElement(
            self.definitions, "bpmn:collaboration", {"id": "Collaboration_1d79bzk"}
        )
        ET.SubElement(
            collaboration,
            "bpmn:participant",
            {
                "id": "Participant_1ddk10v",
                "name": "Pool1",
                "processRef": "Process_16iizmn",
            },
        )

        # Add process
        process = ET.SubElement(
            self.definitions,
            "bpmn:process",
            {"id": "Process_16iizmn", "isExecutable": "false"},
        )

        # Add laneSet
        laneSet = ET.SubElement(process, "bpmn:laneSet", {"id": "LaneSet_018ko9p"})

        # Add lanes
        lane1 = ET.SubElement(
            laneSet, "bpmn:lane", {"id": "Lane_095hyow", "name": "Lane1"}
        )
        ET.SubElement(lane1, "bpmn:flowNodeRef").text = "Activity_0peyiz2"
        ET.SubElement(lane1, "bpmn:flowNodeRef").text = "StartEvent_0fakp1h"

        lane2 = ET.SubElement(
            laneSet, "bpmn:lane", {"id": "Lane_01qd7x5", "name": "Lane2"}
        )
        ET.SubElement(lane2, "bpmn:flowNodeRef").text = "Activity_0zg0hcc"
        ET.SubElement(lane2, "bpmn:flowNodeRef").text = "Event_1ndbaxf"

        # Add tasks and events
        task1 = ET.SubElement(
            process, "bpmn:task", {"id": "Activity_0peyiz2", "name": "task1"}
        )
        ET.SubElement(task1, "bpmn:incoming").text = "Flow_07jnnig"
        ET.SubElement(task1, "bpmn:outgoing").text = "Flow_1v9w12s"

        task2 = ET.SubElement(
            process, "bpmn:task", {"id": "Activity_0zg0hcc", "name": "Task2"}
        )
        ET.SubElement(task2, "bpmn:incoming").text = "Flow_1v9w12s"
        ET.SubElement(task2, "bpmn:outgoing").text = "Flow_1ey5d76"

        endEvent = ET.SubElement(
            process, "bpmn:endEvent", {"id": "Event_1ndbaxf", "name": "stop"}
        )
        ET.SubElement(endEvent, "bpmn:incoming").text = "Flow_1ey5d76"

        startEvent = ET.SubElement(
            process, "bpmn:startEvent", {"id": "StartEvent_0fakp1h", "name": "start"}
        )
        ET.SubElement(startEvent, "bpmn:outgoing").text = "Flow_07jnnig"

        # Add sequence flows
        ET.SubElement(
            process,
            "bpmn:sequenceFlow",
            {
                "id": "Flow_07jnnig",
                "sourceRef": "StartEvent_0fakp1h",
                "targetRef": "Activity_0peyiz2",
            },
        )

        ET.SubElement(
            process,
            "bpmn:sequenceFlow",
            {
                "id": "Flow_1v9w12s",
                "sourceRef": "Activity_0peyiz2",
                "targetRef": "Activity_0zg0hcc",
            },
        )

        ET.SubElement(
            process,
            "bpmn:sequenceFlow",
            {
                "id": "Flow_1ey5d76",
                "sourceRef": "Activity_0zg0hcc",
                "targetRef": "Event_1ndbaxf",
            },
        )

        # Add BPMN diagram
        bpmnDiagram = ET.SubElement(
            self.definitions, "bpmndi:BPMNDiagram", {"id": "BPMNDiagram_1"}
        )
        bpmnPlane = ET.SubElement(
            bpmnDiagram,
            "bpmndi:BPMNPlane",
            {"id": "BPMNPlane_1", "bpmnElement": "Collaboration_1d79bzk"},
        )

        # Add BPMN shapes and edges
        shapes_and_edges = [
            (
                "Participant_1ddk10v_di",
                "Participant_1ddk10v",
                "true",
                {"x": "156", "y": "40", "width": "600", "height": "250"},
                {},
            ),
            (
                "Lane_01qd7x5_di",
                "Lane_01qd7x5",
                "true",
                {"x": "186", "y": "165", "width": "570", "height": "125"},
                {},
            ),
            (
                "Lane_095hyow_di",
                "Lane_095hyow",
                "true",
                {"x": "186", "y": "40", "width": "570", "height": "125"},
                {},
            ),
            (
                "Activity_0peyiz2_di",
                "Activity_0peyiz2",
                None,
                {"x": "340", "y": "60", "width": "100", "height": "80"},
                {
                    "bioc:stroke": "#0d4372",
                    "bioc:fill": "#bbdefb",
                    "color:background-color": "#bbdefb",
                    "color:border-color": "#0d4372",
                },
            ),
            (
                "Activity_0zg0hcc_di",
                "Activity_0zg0hcc",
                None,
                {"x": "340", "y": "190", "width": "100", "height": "80"},
                {},
            ),
            (
                "Event_1ndbaxf_di",
                "Event_1ndbaxf",
                None,
                {"x": "602", "y": "212", "width": "36", "height": "36"},
                {
                    "bpmndi:BPMNLabel": {
                        "dc:Bounds": {
                            "x": "610",
                            "y": "255",
                            "width": "21",
                            "height": "14",
                        }
                    }
                },
            ),
            (
                "_BPMNShape_StartEvent_2",
                "StartEvent_0fakp1h",
                None,
                {"x": "232", "y": "82", "width": "36", "height": "36"},
                {
                    "bpmndi:BPMNLabel": {
                        "dc:Bounds": {
                            "x": "239",
                            "y": "125",
                            "width": "23",
                            "height": "14",
                        }
                    }
                },
            ),
        ]

        for (
            shape_id,
            bpmnElement,
            isHorizontal,
            bounds,
            extra_attrs,
        ) in shapes_and_edges:
            # print(f"{shape_id}")
            shape = ET.SubElement(
                bpmnPlane,
                "bpmndi:BPMNShape",
                {"id": shape_id, "bpmnElement": bpmnElement},
            )
            if isHorizontal:
                shape.set("isHorizontal", isHorizontal)
            ET.SubElement(shape, "dc:Bounds", bounds)
            if extra_attrs:
                for k, v in extra_attrs.items():
                    if isinstance(v, dict):
                        subelement = ET.SubElement(shape, k)
                        for sub_k, sub_v in v.items():
                            ET.SubElement(subelement, sub_k, sub_v)
                    else:
                        shape.set(k, v)

        edges = [
            (
                "Flow_07jnnig_di",
                "Flow_07jnnig",
                [{"x": "268", "y": "100"}, {"x": "340", "y": "100"}],
            ),
            (
                "Flow_1v9w12s_di",
                "Flow_1v9w12s",
                [{"x": "390", "y": "140"}, {"x": "390", "y": "190"}],
            ),
            (
                "Flow_1ey5d76_di",
                "Flow_1ey5d76",
                [{"x": "440", "y": "230"}, {"x": "602", "y": "230"}],
            ),
        ]

        for edge_id, bpmnElement, waypoints in edges:
            edge = ET.SubElement(
                bpmnPlane,
                "bpmndi:BPMNEdge",
                {"id": edge_id, "bpmnElement": bpmnElement},
            )
            for waypoint in waypoints:
                ET.SubElement(edge, "di:waypoint", waypoint)

        # Convert the ElementTree to a string and write to a file
        tree = ET.ElementTree(self.definitions)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)

    def indent(self, elem, level=0):
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = f"{i}    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        elif level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

    def export_to_xml(self, pools, filename):
        """Export the BPMN diagram to XML"""
        print("Exporting..")
        # self.render_sample(pools, filename)

        # ** loop through pools for debugging **
        # for pool in pools:
        #     print(f"{pool.bpmn_id},{pool.name}")
        #     lanes = pool.lanes
        #     for lane in lanes:
        #         print(f"    {lane.bpmn_id},{lane.name}")
        #         shapes = lane.shapes
        #         for shape in shapes:
        #             print(
        #                 f"        {shape.bpmn_id}, {shape.name}, type={type(shape).__name__}"
        #             )

        # ------ (1) Process Section -------
        for pool in pools:
            # *** Generate bpmn:process elements ***
            if pool.name != "Default Pool":
                process = ET.SubElement(
                    self.definitions,
                    "bpmn:process",
                    {"id": pool.bpmn_id, "name": pool.name, "isExecutable": "false"},
                )
            lanes = pool.lanes
            if lanes is not None:
                # *** Generate bpmn:laneSet elements ***
                if pool.name != "Default Pool":
                    lane_set = ET.SubElement(
                        process, "bpmn:laneSet", {"id": Helper.get_uuid()}
                    )

                for lane in lanes:
                    # *** Generate bpmn:lane elements ***
                    if pool.name != "Default Pool":
                        bpmn_lane = ET.SubElement(
                            lane_set,
                            "bpmn:lane",
                            {"id": lane.bpmn_id, "name": lane.name},
                        )
                    else:
                        bpmn_lane = ET.SubElement(
                            self.definitions,
                            "bpmn:process",
                            {"id": lane.bpmn_id, "name": lane.name},
                        )
                        process = bpmn_lane

                    # *** Generate bpmn:flowNodeRef ***
                    shapes = lane.shapes
                    for shape in shapes:
                        # for connection in shape.connection_to:
                        # if shape.is_same_pool(connection.source, connection.target):
                        if pool.name != "Default Pool":
                            flowNodeRef = ET.SubElement(bpmn_lane, "bpmn:flowNodeRef")
                            # add text to flowNodeRef
                            flowNodeRef.text = shape.bpmn_id

                        print(f"{shape.name}, {shape.bpmn_id}")

            for lane in pool.lanes:
                for shape in lane.shapes:
                    # *** Generate bpmn:<task/gateway/event> elements ***
                    # print(f"{shape.name}, {type(shape)}")
                    if type(shape) is Start:
                        ET.SubElement(
                            process,
                            "bpmn:startEvent",
                            {"id": shape.bpmn_id, "name": shape.name},
                        )
                    elif type(shape) is End:
                        ET.SubElement(
                            process,
                            "bpmn:endEvent",
                            {"id": shape.bpmn_id, "name": shape.name},
                        )
                    elif type(shape) is Task:
                        ET.SubElement(
                            process,
                            "bpmn:task",
                            {"id": shape.bpmn_id, "name": shape.name},
                        )
                    elif type(shape) is Exclusive:
                        ET.SubElement(
                            process,
                            "bpmn:exclusiveGateway",
                            {"id": shape.bpmn_id, "name": shape.name},
                        )
                    if shape.connection_to is not None:
                        for connection in shape.connection_to:
                            if shape.is_same_pool(connection.source, connection.target):
                                # *** Generate bpmn:sequenceFlow elements ***
                                sequence_flow = ET.SubElement(
                                    process,
                                    "bpmn:sequenceFlow",
                                    {
                                        "id": connection.bpmn_id,
                                        "name": connection.label,
                                        "sourceRef": shape.bpmn_id,
                                        "targetRef": connection.target.bpmn_id,
                                    },
                                )
                                # connection.bpmn_id = sequence_flow.get("id")

        # ------ (2) Collaboration Section -------
        collaboration_id = ""
        if len(pools) > 1:
            # *** Generate bpmn:collaboration element ***
            collaboration = ET.SubElement(
                self.definitions, "bpmn:collaboration", {"id": Helper.get_uuid()}
            )
            # get collaboration id
            collaboration_id = collaboration.get("id")

            for pool in pools:
                # *** Generate bpmn:participant element ***
                if pool.name != "Default Pool":
                    bpmn_participant = ET.SubElement(
                        collaboration,
                        "bpmn:participant",
                        {
                            "id": Helper.get_uuid(),
                            "name": pool.name,
                            "processRef": pool.bpmn_id,
                        },
                    )
                    pool.bpmn_collaboration_id = bpmn_participant.get("id")

                # *** Generate bpmn:messageFlow elements ***
                for lane in pool.lanes:
                    if pool.name == "Default Pool":
                        bpmn_participant = ET.SubElement(
                            collaboration,
                            "bpmn:participant",
                            {
                                "id": Helper.get_uuid(),
                                "name": lane.name,
                                "processRef": lane.bpmn_id,
                            },
                        )
                        lane.bpmn_collaboration_id = bpmn_participant.get("id")
                    for shape in lane.shapes:
                        if shape.connection_to is not None:
                            for connection in shape.connection_to:
                                if not shape.is_same_pool(
                                    connection.source, connection.target
                                ):
                                    ET.SubElement(
                                        collaboration,
                                        "bpmn:messageFlow",
                                        {
                                            "id": connection.bpmn_id,
                                            "name": connection.label,
                                            "sourceRef": shape.bpmn_id,
                                            "targetRef": connection.target.bpmn_id,
                                        },
                                    )

        # *** (3) BPMN Diagram Section
        # *** Generate bpmndi:BPMNDiagram Elements ***
        bpmn_diagram = ET.SubElement(
            self.definitions,
            "bpmndi:BPMNDiagram",
            {"id": Helper.get_uuid(), "name": "BPMN Diagram"},
        )
        # *** Generate bpmndi:BPMNPlane Elements ***
        bpmn_plane = ET.SubElement(
            bpmn_diagram,
            "bpmndi:BPMNPlane",
            {"id": Helper.get_uuid(), "bpmnElement": collaboration_id},
        )

        for pool in pools:
            if pool.name != "Default Pool":
                bpmn_shape = ET.SubElement(
                    bpmn_plane,
                    "bpmndi:BPMNShape",
                    {
                        "id": Helper.get_uuid(),
                        "bpmnElement": pool.bpmn_collaboration_id,
                        # "bpmnElement": pool.bpmn_id,
                        "color:background-color": pool.fill_colour,
                    },
                )
                # *** Generate dc:Bounds Elements ***
                ET.SubElement(
                    bpmn_shape,
                    "dc:Bounds",
                    {
                        "x": str(pool.coord.x_pos),
                        "y": str(pool.coord.y_pos),
                        "width": str(pool.width),
                        "height": str(pool.height),
                    },
                )
            for lane in pool.lanes:
                if pool.name == "Default Pool":
                    bpmn_shape = ET.SubElement(
                        bpmn_plane,
                        "bpmndi:BPMNShape",
                        {
                            "id": Helper.get_uuid(),
                            "bpmnElement": lane.bpmn_collaboration_id,
                        },
                    )
                    # *** Generate dc:Bounds Elements ***
                    ET.SubElement(
                        bpmn_shape,
                        "dc:Bounds",
                        {
                            "x": str(lane.coord.x_pos),
                            "y": str(lane.coord.y_pos),
                            "width": str(lane.width),
                            "height": str(lane.height),
                        },
                    )
                else:
                    bpmn_shape = ET.SubElement(
                        bpmn_plane,
                        "bpmndi:BPMNShape",
                        {"id": Helper.get_uuid(), "bpmnElement": lane.bpmn_id},
                    )
                    # *** Generate dc:Bounds Elements ***
                    ET.SubElement(
                        bpmn_shape,
                        "dc:Bounds",
                        {
                            "x": str(lane.coord.x_pos),
                            "y": str(lane.coord.y_pos),
                            "width": str(lane.width),
                            "height": str(lane.height),
                        },
                    )

                for shape in lane.shapes:
                    if (
                        type(shape) is Start
                        or type(shape) is End
                        or type(shape) is Task
                        or type(shape) is Exclusive
                    ):
                        # *** Generate bpmndi:BPMNShape Elements ***
                        bpmn_shape = ET.SubElement(
                            bpmn_plane,
                            "bpmndi:BPMNShape",
                            {
                                "id": Helper.get_uuid(),
                                "bpmnElement": shape.bpmn_id,
                                "color:background-color": shape.fill_colour,
                            },
                        )
                        # *** Generate dc:Bounds Elements ***
                        if type(shape) is Start or type(shape) is End:
                            ET.SubElement(
                                bpmn_shape,
                                "dc:Bounds",
                                {
                                    "x": str(shape.coord.x_pos - shape.radius),
                                    "y": str(shape.coord.y_pos - shape.radius),
                                    "width": str(shape.width),
                                    "height": str(shape.height),
                                },
                            )
                        else:
                            ET.SubElement(
                                bpmn_shape,
                                "dc:Bounds",
                                {
                                    "x": str(shape.coord.x_pos),
                                    "y": str(shape.coord.y_pos),
                                    "width": str(shape.width),
                                    "height": str(shape.height),
                                },
                            )
                        print(
                            f"{shape.name}, {shape.coord.x_pos}, {shape.coord.y_pos}, {shape.origin_coord.x_pos}, {shape.origin_coord.y_pos}"
                        )

                        # Generate BPMNEdge
                        if shape.connection_to is not None:
                            for connection in shape.connection_to:
                                # *** Generate bpmndi:BPMNEdge Elements ***
                                bpmn_edge = ET.SubElement(
                                    bpmn_plane,
                                    "bpmndi:BPMNEdge",
                                    {
                                        "id": Helper.get_uuid(),
                                        "bpmnElement": connection.bpmn_id,
                                    },
                                )
                                # *** Generate di:waypoint Elements ***

                                print(
                                    f"    *** {bpmn_edge.get('id')}, {connection.source.name} -> {connection.target.name}"
                                )

                                if len(connection.connection_points) > 0:
                                    print(f"        === {connection.connection_points}")
                                    # print(f"=== {connection.source.outgoing_points[0][0]}, {connection.target.incoming_points[0]}")
                                    for x_pos, y_pos in connection.connection_points:
                                        print(
                                            f"          outgoing waypoint: {x_pos}, {y_pos}, {connection.target.name}"
                                        )
                                        ET.SubElement(
                                            bpmn_edge,
                                            "di:waypoint",
                                            {
                                                "x": str(x_pos),
                                                "y": str(y_pos),
                                            },
                                        )

        # Identify Diagram : BPMNDiagram (id, name)
        #   b. BPMNLabelStyle (id, labelStyle)
        #       i. dc:Font (name, size, isBold, isItalic, isUnderline, isStrikeThrough)

        tree = ET.ElementTree(self.definitions)
        self.indent(self.definitions)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    bpmn = BPMN()
    bpmn.export_to_xml()
