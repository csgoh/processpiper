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
from typing import List, Dict, Any, Optional
from .shape import Shape
from .event import Start, End
from .activity import Task
from .gateway import Exclusive
from .helper import Helper
from .version import __version__

BPMN_NAMESPACE = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMN_DI_NAMESPACE = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NAMESPACE = "http://www.omg.org/spec/DD/20100524/DC"
DI_NAMESPACE = "http://www.omg.org/spec/DD/20100524/DI"
BIOC_NAMESPACE = "http://bpmn.io/schema/bpmn/biocolor/1.0"
COLOR_NAMESPACE = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"


class XMLExporter:
    def create_root_element(self) -> ET.Element:
        return ET.Element("bpmn:definitions", self._get_root_attributes())

    def _get_root_attributes(self) -> Dict[str, str]:
        return {
            "id": f"Definitions_{Helper.get_uuid()}",
            "targetNamespace": "https://github.com/csgoh/processpiper/schema/bpmn",
            "exporter": "ProcessPiper (https://github.com/csgoh/processpiper)",
            "exporterVersion": __version__,
            "xmlns:bpmn": BPMN_NAMESPACE,
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:bpmndi": BPMN_DI_NAMESPACE,
            "xmlns:dc": DC_NAMESPACE,
            "xmlns:di": DI_NAMESPACE,
            "xmlns:bioc": BIOC_NAMESPACE,
            "xmlns:color": COLOR_NAMESPACE,
        }

    def write_to_file(self, root: ET.Element, filename: str) -> None:
        self._indent(root)
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)

    def _indent(self, elem: ET.Element, level: int = 0) -> None:
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = f"{i}    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        elif level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class BPMNElementCreator:
    def _add_process_element(self, parent: ET.Element, pool: Any):
        return ET.SubElement(
            parent,
            "bpmn:process",
            {"id": pool.bpmn_id, "name": pool.name, "isExecutable": "false"},
        )

    def _add_laneset_element(self, parent: ET.Element, id: str):
        return ET.SubElement(parent, "bpmn:laneSet", {"id": id})

    def _add_lane_element(self, parent: ET.Element, lane: Any):
        return ET.SubElement(
            parent, "bpmn:lane", {"id": lane.bpmn_id, "name": lane.name}
        )

    def _add_flowNodeRef(self, parent: ET.Element, id: str):
        ET.SubElement(parent, "bpmn:flowNodeRef").text = id

    def _add_start_event(self, parent: ET.Element, shape: Start):
        self._add_sub_element(parent, "bpmn:startEvent", shape)

    def _add_end_event(self, parent: ET.Element, shape: End):
        self._add_sub_element(parent, "bpmn:endEvent", shape)

    def _add_task(self, parent: ET.Element, shape: Task):
        self._add_sub_element(parent, "bpmn:task", shape)

    def _add_exclusive_gateway(self, parent: ET.Element, shape: Exclusive):
        self._add_sub_element(parent, "bpmn:exclusiveGateway", shape)

    def _add_sub_element(self, parent: ET.Element, bpmn_element: str, shape: Any):
        ET.SubElement(
            parent,
            bpmn_element,
            {"id": shape.bpmn_id, "name": shape.name},
        )

    def _add_sequence_flow(
        self, parent: ET.Element, id: str, name: str, source: str, target: str
    ):
        ET.SubElement(
            parent,
            "bpmn:sequenceFlow",
            {"id": id, "name": name, "sourceRef": source, "targetRef": target},
        )

    def _add_collaboration_element(self, parent: ET.Element, id: str):
        return ET.SubElement(parent, "bpmn:collaboration", {"id": id})

    def _add_participant_element(self, parent: ET.Element, id: str, pool: Any):
        return ET.SubElement(
            parent,
            "bpmn:participant",
            {
                "id": Helper.get_uuid(),
                "name": pool.name,
                "processRef": pool.bpmn_id,
            },
        )

    def _add_messageflow_element(self, parent: ET.Element, connection: Any):
        ET.SubElement(
            parent,
            "bpmn:messageFlow",
            {
                "id": connection.bpmn_id,
                "name": connection.label,
                "sourceRef": connection.source.bpmn_id,
                "targetRef": connection.target.bpmn_id,
            },
        )

    def _add_diagram_element(self, parent: ET.Element):
        return ET.SubElement(
            parent,
            "bpmndi:BPMNDiagram",
            {"id": Helper.get_uuid(), "name": "BPMN Diagram"},
        )

    def _add_plane_element(self, parent: ET.Element, collaboration_id: str):
        return ET.SubElement(
            parent,
            "bpmndi:BPMNPlane",
            {"id": Helper.get_uuid(), "bpmnElement": collaboration_id},
        )

    def _add_shape_element(
        self,
        parent: ET.Element,
        element: Any,
        collaboration_id: str,
        fill_background_colour: bool,
    ):
        if fill_background_colour:
            bpmn_shape = ET.SubElement(
                parent,
                "bpmndi:BPMNShape",
                {
                    "id": Helper.get_uuid(),
                    "bpmnElement": collaboration_id,
                    # "bpmnElement": pool.bpmn_id,
                    "color:background-color": element.fill_colour,
                },
            )
        else:
            bpmn_shape = ET.SubElement(
                parent,
                "bpmndi:BPMNShape",
                {
                    "id": Helper.get_uuid(),
                    "bpmnElement": collaboration_id,
                },
            )
        # *** Generate dc:Bounds Elements ***
        if type(element) is Start or type(element) is End:
            ET.SubElement(
                bpmn_shape,
                "dc:Bounds",
                {
                    "x": str(element.coord.x_pos - element.radius),
                    "y": str(element.coord.y_pos - element.radius),
                    "width": str(element.width),
                    "height": str(element.height),
                },
            )
        else:
            ET.SubElement(
                bpmn_shape,
                "dc:Bounds",
                {
                    "x": str(element.coord.x_pos),
                    "y": str(element.coord.y_pos),
                    "width": str(element.width),
                    "height": str(element.height),
                },
            )
        return bpmn_shape

    def _add_edge_element(self, parent: ET.Element, connection: Any):
        return ET.SubElement(
            parent,
            "bpmndi:BPMNEdge",
            {
                "id": Helper.get_uuid(),
                "bpmnElement": connection.bpmn_id,
            },
        )

    def _add_waypoint_element(self, parent: ET.Element, x_pos: int, y_pos: int):
        return ET.SubElement(
            parent,
            "di:waypoint",
            {
                "x": str(x_pos),
                "y": str(y_pos),
            },
        )

    def create_process_section(self, root: ET.Element, pools: list[Any]):
        for pool in pools:
            # *** Generate bpmn:process elements ***
            if pool.has_pool():
                process = self._add_process_element(root, pool)
            else:
                # *** If Default Pool, lane is pool.
                lane = pool.lanes[0]
                process = self._add_process_element(root, lane)

            lanes = pool.lanes

            if lanes is not None:
                # *** Generate bpmn:laneSet elements ***
                if pool.has_pool():  # *** Only pool has laneSet and lane
                    lane_set = self._add_laneset_element(process, Helper.get_uuid())

                for lane in lanes:
                    # *** Generate bpmn:lane elements ***
                    if pool.has_pool():
                        bpmn_lane = self._add_lane_element(lane_set, lane)

                    # *** Generate bpmn:flowNodeRef ***
                    shapes = lane.shapes
                    for shape in shapes:
                        if pool.has_pool():
                            self._add_flowNodeRef(bpmn_lane, shape.bpmn_id)

                    for shape in lane.shapes:
                        # *** Generate bpmn event, activity, gateway elements
                        if type(shape) is Start:
                            self._add_start_event(process, shape)
                        elif type(shape) is End:
                            self._add_end_event(process, shape)
                        elif type(shape) is Task:
                            self._add_task(process, shape)
                        elif type(shape) is Exclusive:
                            self._add_exclusive_gateway(process, shape)
                        if shape.connection_to is not None:
                            for connection in shape.connection_to:
                                if shape.is_same_pool(
                                    connection.source, connection.target
                                ):
                                    # *** Generate bpmn:sequenceFlow elements ***
                                    self._add_sequence_flow(
                                        process,
                                        connection.bpmn_id,
                                        connection.label,
                                        connection.source.bpmn_id,
                                        connection.target.bpmn_id,
                                    )

    def create_collaboration_section(self, root: ET.Element, pools: list[Any]) -> str:
        collaboration_id = ""
        if (
            len(pools) > 1
        ):  # *** Only generate collaboration if there are more than one pool
            # *** Generate bpmn:collaboration element ***
            collaboration = self._add_collaboration_element(root, Helper.get_uuid())
            collaboration_id = collaboration.get("id")

            for pool in pools:
                # *** Generate bpmn:participant element ***
                if pool.has_pool():
                    bpmn_participant = self._add_participant_element(
                        collaboration, Helper.get_uuid(), pool
                    )
                    pool.bpmn_collaboration_id = bpmn_participant.get("id")
                else:  # ** lane only pool
                    bpmn_participant = self._add_participant_element(
                        collaboration, Helper.get_uuid(), pool.lanes[0]
                    )
                    pool.lanes[0].bpmn_collaboration_id = bpmn_participant.get("id")

                # *** Generate bpmn:messageFlow elements ***
                for lane in pool.lanes:
                    for shape in lane.shapes:
                        if shape.connection_to is not None:
                            for connection in shape.connection_to:
                                if not shape.is_same_pool(
                                    connection.source, connection.target
                                ):
                                    self._add_messageflow_element(
                                        collaboration,
                                        connection,
                                    )
        return collaboration_id

    def create_diagram_section(
        self, root: ET.Element, pools: list[Any], collaboration_id: str
    ):
        # *** Generate bpmndi:BPMNDiagram Element ***
        bpmn_diagram = self._add_diagram_element(root)

        # *** Generate bpmndi:BPMNPlane Element ***
        bpmn_plane = self._add_plane_element(bpmn_diagram, collaboration_id)

        for pool in pools:
            if pool.has_pool():
                # *** Add shape for pool ***
                self._add_shape_element(
                    bpmn_plane, pool, pool.bpmn_collaboration_id, True
                )

            for lane in pool.lanes:
                if pool.has_lane_only():
                    # *** Add shape for lane ***
                    self._add_shape_element(
                        bpmn_plane, lane, lane.bpmn_collaboration_id, False
                    )
                else:
                    self._add_shape_element(bpmn_plane, lane, lane.bpmn_id, False)

                for shape in lane.shapes:
                    # *** Generate bpmndi:BPMNShape Elements ***
                    self._add_shape_element(bpmn_plane, shape, shape.bpmn_id, True)
                    print(
                        f"{shape.name}, {shape.coord.x_pos}, {shape.coord.y_pos}, {shape.origin_coord.x_pos}, {shape.origin_coord.y_pos}"
                    )

                    # Generate BPMNEdge
                    if shape.connection_to is not None:
                        for connection in shape.connection_to:
                            # *** Generate bpmndi:BPMNEdge Elements ***
                            bpmn_edge = self._add_edge_element(bpmn_plane, connection)
                            print(
                                f"    *** {bpmn_edge.get('id')}, {connection.source.name} -> {connection.target.name}"
                            )

                            if len(connection.connection_points) > 0:
                                print(f"        === {connection.connection_points}")
                                for x_pos, y_pos in connection.connection_points:
                                    print(
                                        f"          outgoing waypoint: {x_pos}, {y_pos}, {connection.target.name}"
                                    )
                                    self._add_waypoint_element(bpmn_edge, x_pos, y_pos)


@dataclass
class BPMN:
    """BPMN diagram"""

    id: str = field(init=False)
    name: str = field(init=False)

    _pools: list = field(init=False, default_factory=list)

    def __post_init__(self):
        self.xml_exporter = XMLExporter()
        self.element_creator = BPMNElementCreator()

    def export_to_xml(self, pools, filename):
        """Export the BPMN diagram to XML"""
        print("Exporting diagram to .bpmn format..")

        root = self.xml_exporter.create_root_element()

        # ------ (1) Process Section -------
        self.element_creator.create_process_section(root, pools)

        # ------ (2) Collaboration Section -------
        collaboration_id = self.element_creator.create_collaboration_section(
            root, pools
        )

        # ------ (3) BPMN Diagram Section ------
        self.element_creator.create_diagram_section(root, pools, collaboration_id)

        self.xml_exporter.write_to_file(root, filename)


if __name__ == "__main__":
    bpmn = BPMN()
    bpmn.export_to_xml()
