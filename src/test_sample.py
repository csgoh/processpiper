from .processpiper import ProcessMap, EventType, ActivityType, GatewayType
from .processpiper import text2diagram


def test_sample01():
    with ProcessMap(
        "debug01", colour_theme="BLUEMOUNTAIN", width=8192
    ) as my_process_map:
        with my_process_map.add_lane("customer") as lane1:
            start = lane1.add_element("start", EventType.START)
            activity_9 = lane1.add_element(
                "brings a defective computer", ActivityType.TASK
            )
        with my_process_map.add_lane("crs") as lane2:
            activity_10 = lane2.add_element("checks the defect", ActivityType.TASK)
            activity_11 = lane2.add_element(
                "hand out a repair cost calculation", ActivityType.TASK
            )
            gateway_1 = lane2.add_element("the customer decide", GatewayType.EXCLUSIVE)
            activity_3 = lane2.add_element("are acceptable", ActivityType.TASK)
            activity_4 = lane2.add_element("continues", ActivityType.TASK)
            activity_5 = lane2.add_element("takes her computer", ActivityType.TASK)
            activity_12 = lane2.add_element(
                "consists of two activities", ActivityType.TASK
            )
            activity_13 = lane2.add_element(
                "execute two activities in an arbitrary order", ActivityType.TASK
            )
            activity_14 = lane2.add_element("is", ActivityType.TASK)
            activity_15 = lane2.add_element("check the hardware", ActivityType.TASK)
            activity_16 = lane2.add_element("repair the hardware", ActivityType.TASK)
            activity_17 = lane2.add_element("checks the software", ActivityType.TASK)
            activity_18 = lane2.add_element("configure the software", ActivityType.TASK)
            activity_19 = lane2.add_element(
                "test the proper system functionality after each of these activities",
                ActivityType.TASK,
            )
            gateway_6 = lane2.add_element("detect an error", GatewayType.EXCLUSIVE)
            activity_8 = lane2.add_element(
                "execute another arbitrary repair activity", ActivityType.TASK
            )
            end = lane2.add_element("end", EventType.END)
            start.connect(activity_9)
            activity_9.connect(activity_10)
            activity_10.connect(activity_11)
            activity_11.connect(gateway_1)
            gateway_1.connect(activity_3)
            activity_3.connect(activity_4)
            activity_4.connect(activity_12)
            gateway_1.connect(activity_5)
            activity_5.connect(activity_12)
            activity_12.connect(activity_13)
            activity_13.connect(activity_14)
            activity_14.connect(activity_15)
            activity_15.connect(activity_16)
            activity_16.connect(activity_17)
            activity_17.connect(activity_18)
            activity_18.connect(activity_19)
            activity_19.connect(gateway_6)
            gateway_6.connect(activity_8)
            activity_8.connect(end)
            gateway_6.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample01.png")


def test_sample02():
    with ProcessMap(
        "debug", colour_theme="BLUEMOUNTAIN", width=10000
    ) as my_process_map:
        with my_process_map.add_pool("Pool") as pool1:
            with pool1.add_lane("lane1") as lane1:
                start = lane1.add_element("start", EventType.START)
                t5 = lane1.add_element(
                    "T5",
                    ActivityType.TASK,
                )
                end = lane1.add_element("end", EventType.END)
                t1 = lane1.add_element("T1", ActivityType.TASK)
                gateway_1 = lane1.add_element("G1", GatewayType.EXCLUSIVE)
                gateway_2 = lane1.add_element("G2", GatewayType.EXCLUSIVE)
                t4 = lane1.add_element("T4", ActivityType.TASK)
                t2 = lane1.add_element("T2", ActivityType.TASK)
                t3 = lane1.add_element("T3", ActivityType.TASK)
                gateway_2_end = lane1.add_element("G2E", GatewayType.EXCLUSIVE)
                gateway_1_end = lane1.add_element("G1E", GatewayType.EXCLUSIVE)
            start.connect(t1)
            t1.connect(gateway_1)
            gateway_1.connect(gateway_2)
            gateway_1.connect(t2, "msg1")
            gateway_2.connect(t4)
            gateway_2.connect(t3, "msg2")
            t3.connect(gateway_2_end)
            t4.connect(gateway_2_end)
            gateway_2_end.connect(gateway_1_end, "msg3")
            t2.connect(gateway_1_end, "t2msg")
            gateway_1_end.connect(t5)
            t5.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample02.png")


def test_sample03():
    with ProcessMap(
        "Break Glass Process", colour_theme="BLUEMOUNTAIN"
    ) as my_process_map:
        with my_process_map.add_pool("Organisation") as pool1:
            with pool1.add_lane("ProductA User") as lane1:
                start = lane1.add_element("start", EventType.START)
                report_issue = lane1.add_element(
                    "Report connectivity issue", ActivityType.TASK
                )
            with pool1.add_lane("Service Desk") as lane2:
                triage = lane2.add_element("Triage", ActivityType.TASK)
                azure_ad_issue = lane2.add_element(
                    "Azure AD issue?", GatewayType.EXCLUSIVE
                )
                escalate_ist = lane2.add_element(
                    "Escalate to IST team", ActivityType.TASK
                )
                escalate_producta = lane2.add_element(
                    "Escalate to ProductA team", ActivityType.TASK
                )
                notify_user = lane2.add_element("Notify user", ActivityType.TASK)
                close_ticket = lane2.add_element("close", EventType.END)
            with pool1.add_lane("ProductA Administrator") as lane3:
                verify_issue = lane3.add_element(
                    "Verify Azure AD Authentication Issue", ActivityType.TASK
                )
                contact_esd = lane3.add_element(
                    "Notify Vendor Service Desk", ActivityType.TASK
                )
                get_approval = lane3.add_element(
                    "Get break glass approval", ActivityType.TASK
                )
                document_approval = lane3.add_element(
                    "Document reason and approval", ActivityType.TASK
                )
                access_account = lane3.add_element(
                    "Access to break glass account", ActivityType.TASK
                )
                notify_service_desk = lane3.add_element(
                    "Notify Service Desk", ActivityType.TASK
                )
                logout_account = lane3.add_element(
                    "logout from break glass account", ActivityType.TASK
                )
                end = lane3.add_element("end", EventType.END)
        with my_process_map.add_pool("Vendor") as pool2:
            with pool2.add_lane("Service Desk") as lane4:
                fix_connectivity = lane4.add_element(
                    "Fix authentication issue", ActivityType.TASK
                )
                notify_admin = lane4.add_element(
                    "Notify ProductA Administrator", ActivityType.TASK
                )
            start.connect(report_issue)
            report_issue.connect(triage)
            triage.connect(azure_ad_issue)
            azure_ad_issue.connect(escalate_ist, "Yes")
            azure_ad_issue.connect(escalate_producta, "No")
            escalate_producta.connect(verify_issue)
            verify_issue.connect(contact_esd)
            contact_esd.connect(get_approval)
            get_approval.connect(document_approval)
            document_approval.connect(access_account)
            contact_esd.connect(fix_connectivity)
            fix_connectivity.connect(notify_admin)
            notify_admin.connect(notify_service_desk)
            notify_service_desk.connect(notify_user)
            notify_user.connect(close_ticket)
            access_account.connect(logout_account)
            logout_account.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample03.png")


def test_sample04():
    with ProcessMap(
        "Break Glass Process", colour_theme="BLUEMOUNTAIN", painter_type="SVG"
    ) as my_process_map:
        with my_process_map.add_pool("Organisation") as pool1:
            with pool1.add_lane("ProductA User") as lane1:
                start = lane1.add_element("start", EventType.START)
                report_issue = lane1.add_element(
                    "Report connectivity issue", ActivityType.TASK
                )
            with pool1.add_lane("Service Desk") as lane2:
                triage = lane2.add_element("Triage", ActivityType.TASK)
                azure_ad_issue = lane2.add_element(
                    "Azure AD issue?", GatewayType.EXCLUSIVE
                )
                escalate_ist = lane2.add_element(
                    "Escalate to IST team", ActivityType.TASK
                )
                escalate_producta = lane2.add_element(
                    "Escalate to ProductA team", ActivityType.TASK
                )
                notify_user = lane2.add_element("Notify user", ActivityType.TASK)
                close_ticket = lane2.add_element("close", EventType.END)
            with pool1.add_lane("ProductA Administrator") as lane3:
                verify_issue = lane3.add_element(
                    "Verify Azure AD Authentication Issue", ActivityType.TASK
                )
                contact_esd = lane3.add_element(
                    "Notify Vendor Service Desk", ActivityType.TASK
                )
                get_approval = lane3.add_element(
                    "Get break glass approval", ActivityType.TASK
                )
                document_approval = lane3.add_element(
                    "Document reason and approval", ActivityType.TASK
                )
                access_account = lane3.add_element(
                    "Access to break glass account", ActivityType.TASK
                )
                notify_service_desk = lane3.add_element(
                    "Notify Service Desk", ActivityType.TASK
                )
                logout_account = lane3.add_element(
                    "logout from break glass account", ActivityType.TASK
                )
                end = lane3.add_element("end", EventType.END)
        with my_process_map.add_pool("Vendor") as pool2:
            with pool2.add_lane("Service Desk") as lane4:
                fix_connectivity = lane4.add_element(
                    "Fix authentication issue", ActivityType.TASK
                )
                notify_admin = lane4.add_element(
                    "Notify ProductA Administrator", ActivityType.TASK
                )
            start.connect(report_issue)
            report_issue.connect(triage)
            triage.connect(azure_ad_issue)
            azure_ad_issue.connect(escalate_ist, "Yes")
            azure_ad_issue.connect(escalate_producta, "No")
            escalate_producta.connect(verify_issue)
            verify_issue.connect(contact_esd)
            contact_esd.connect(get_approval)
            get_approval.connect(document_approval)
            document_approval.connect(access_account)
            contact_esd.connect(fix_connectivity)
            fix_connectivity.connect(notify_admin)
            notify_admin.connect(notify_service_desk)
            notify_service_desk.connect(notify_user)
            notify_user.connect(close_ticket)
            access_account.connect(logout_account)
            logout_account.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample04.svg")


def test_sample05():
    with ProcessMap(
        "Test Max Connection Process", colour_theme="BLUEMOUNTAIN", painter_type="SVG"
    ) as my_process_map:
        with my_process_map.add_lane("Test Lane") as lane1:
            start = lane1.add_element("start", EventType.START)
            t1 = lane1.add_element("Task 1", ActivityType.TASK)
            t2 = lane1.add_element("Task 2", ActivityType.TASK)
            t3 = lane1.add_element("Task 3", ActivityType.TASK)
            t4 = lane1.add_element("Task 4", ActivityType.TASK)
            t5 = lane1.add_element("Task 5", ActivityType.TASK)
            t6 = lane1.add_element("Task 6", ActivityType.TASK)
            end = lane1.add_element("end", EventType.END)

            start.connect(t1)
            t1.connect(t2)
            t1.connect(t3)
            t1.connect(t4)
            t1.connect(t5)
            t1.connect(t6)
            t6.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample05.svg")


def test_sample06():
    with ProcessMap(
        "Test Max Connection Process", colour_theme="BLUEMOUNTAIN", painter_type="SVG"
    ) as my_process_map:
        with my_process_map.add_lane("Test Lane") as lane1:
            start = lane1.add_element("start", EventType.START)
            t1 = lane1.add_element("Task 1", ActivityType.TASK)
            g1 = lane1.add_element("Gateway 1", GatewayType.EXCLUSIVE)
            g2 = lane1.add_element("Gateway 2", GatewayType.EXCLUSIVE)

            t2 = lane1.add_element("Task 2", ActivityType.TASK)
            t3 = lane1.add_element("Task 3", ActivityType.TASK)
            t4 = lane1.add_element("Task 4", ActivityType.TASK)
            t5 = lane1.add_element("Task 5", ActivityType.TASK)
            t51 = lane1.add_element("Task 5.1", ActivityType.TASK)
            t6 = lane1.add_element("Task 6", ActivityType.TASK)
            end = lane1.add_element("end", EventType.END)

            start.connect(t1)
            t1.connect(g1)
            g1.connect(t2)
            g1.connect(t3)
            g1.connect(g2)
            g2.connect(t4)
            g2.connect(t5)
            g2.connect(t51)
            t2.connect(t6)
            t3.connect(t6)
            t4.connect(t6)
            t5.connect(t6)
            t51.connect(t6)
            t6.connect(end)
        my_process_map.draw()
        my_process_map.save("images/test/test_sample06.svg")


def test_sample07():
    with ProcessMap(
        "Product Feature Interface", colour_theme="BLUEMOUNTAIN"
    ) as my_process_map:
        with my_process_map.add_lane("system") as lane_system:
            node_Initiative = lane_system.add_element("Initiative", ActivityType.TASK)
            node_SI = lane_system.add_element("SI", ActivityType.TASK)
            node_Feature = lane_system.add_element("Feature", ActivityType.TASK)

            node_Figma_Design = lane_system.add_element(
                "Figma Design", ActivityType.TASK
            )
            node_Story = lane_system.add_element("Story", ActivityType.TASK)
            node_Product = lane_system.add_element("Product", ActivityType.TASK)
            node_Bug = lane_system.add_element("Bug", ActivityType.TASK)

            g2 = lane_system.add_element("g2", GatewayType.INCLUSIVE)

            g2.connect(node_Figma_Design)
            g1 = lane_system.add_element("g1", GatewayType.INCLUSIVE)
            g1.connect(g2)

            g8 = lane_system.add_element("g8", GatewayType.INCLUSIVE)
            node_Feature.connect(g8, "")

            g9 = lane_system.add_element("g9", GatewayType.INCLUSIVE)
            g9.connect(node_Product, "")

        with my_process_map.add_pool("Product What") as pool_Product_What:
            with pool_Product_What.add_lane("PrSL") as lane_Product_What_PrSL:
                node_Product_feature_is_d = lane_Product_What_PrSL.add_element(
                    "Product feature is defined\nwith acceptance Criteria",
                    ActivityType.TASK,
                )
                node_Product_feature_is_d.connect(node_SI, "")
                node_Initiative.connect(node_Product_feature_is_d, "")

        with pool_Product_What.add_lane("CSB") as lane_Product_What_CSB:
            node_Product_feature_is_c = lane_Product_What_CSB.add_element(
                "Product feature is claried in\nbusiness requirements",
                ActivityType.TASK,
            )
            g7 = lane_Product_What_CSB.add_element("g7", GatewayType.INCLUSIVE)
            node_Product_feature_is_c.connect(g7, "")
            g7.connect(node_Feature, "")
            node_SI.connect(node_Product_feature_is_c, "")

        with my_process_map.add_pool("Product How") as pool_Product_How:
            with pool_Product_How.add_lane("UXD ; CSB") as lane_Product_How_UXD__CSB:
                node_Collaboratively_deve = lane_Product_How_UXD__CSB.add_element(
                    "Collaboratively develop UX\nDesigns with CSB", ActivityType.TASK
                )

                node_Collaboratively_deve.connect(g1, "")
                g8.connect(node_Collaboratively_deve, "")

            with pool_Product_How.add_lane("CSB ; LRC") as lane_Product_How_CSB__LRC:
                node_Review_Figma_Design_ = lane_Product_How_CSB__LRC.add_element(
                    "Review Figma Design with LRC", ActivityType.TASK
                )
                node_Review_Figma_Design_.connect(g1, "")
                node_Figma_Design.connect(node_Review_Figma_Design_, "")

            with pool_Product_How.add_lane("UXD") as lane_Product_How_UXD:
                node_Update_Figma_Design_ = lane_Product_How_UXD.add_element(
                    "Update Figma Design based on\nLRC feedback", ActivityType.TASK
                )
                node_Update_Figma_Design_.connect(g2, "")
                g3 = lane_Product_How_UXD.add_element("g3", GatewayType.INCLUSIVE)
                g3.connect(node_Update_Figma_Design_, "")

            with pool_Product_How.add_lane(
                "Brokerage Squad; UXD"
            ) as lane_Product_How_Brokerage_Squad__UXD:
                node_Work_with_Domains_SL = lane_Product_How_Brokerage_Squad__UXD.add_element(
                    "Work with Domains SL (Bob\nTaiani, Chris Coale) to\ndevelop features UI stories",
                    ActivityType.TASK,
                )
                node_Work_with_Domains_SL.connect(node_Story, "")

                g3.connect(node_Work_with_Domains_SL)

                node_Figma_Design.connect(g3, "")

            with pool_Product_How.add_lane("CSB") as lane_Product_How_CSB:
                node_Create_feature_test_ = lane_Product_How_CSB.add_element(
                    "Create feature test cases", ActivityType.TASK
                )
                node_Create_feature_test_.connect(g7, "")
                g4 = lane_Product_How_CSB.add_element("g4", GatewayType.INCLUSIVE)
                g8.connect(g4, "")
                g4.connect(node_Create_feature_test_, "")

            with pool_Product_How.add_lane(
                "Brokerage Squad"
            ) as lane_Product_How_Brokerage_Squad:
                node_Implement_feature_UI = (
                    lane_Product_How_Brokerage_Squad.add_element(
                        "Implement feature UI stories", ActivityType.TASK
                    )
                )
                node_Implement_feature_UI.connect(g9, "")
                node_Story.connect(node_Implement_feature_UI, "")
                g5 = lane_Product_How_Brokerage_Squad.add_element(
                    "g5", GatewayType.INCLUSIVE
                )
                g2.connect(g5)
                g5.connect(node_Implement_feature_UI, "")
                node_Verify_UI_in_virtual = lane_Product_How_UXD.add_element(
                    "Verify UI in virtual ui test\nenvironment implemented as\nspeced in Figma Design",
                    ActivityType.TASK,
                )
                g5.connect(node_Verify_UI_in_virtual, "")
                node_Verify_UI_in_virtual.connect(node_Bug, "")
                node_Product.connect(node_Verify_UI_in_virtual, "")
                node_Modify_screens_based = (
                    lane_Product_How_Brokerage_Squad.add_element(
                        "Modify screens based on UXD\nfeedback", ActivityType.TASK
                    )
                )
                node_Modify_screens_based.connect(g9, "")
                g6 = lane_Product_How_Brokerage_Squad.add_element(
                    "g6", GatewayType.INCLUSIVE
                )
                g6.connect(node_Modify_screens_based, "")
                node_Bug.connect(g6, "")
                node_Product.connect(g6, "")
                node_Validate_that_Produc = lane_Product_How_CSB.add_element(
                    "Validate that Product meets\ncustomer needs per spec",
                    ActivityType.TASK,
                )
                node_Validate_that_Produc.connect(node_Bug, "")
                node_Feature.connect(node_Validate_that_Produc, "")
                node_Modify_screens_based = (
                    lane_Product_How_Brokerage_Squad.add_element(
                        "Modify screens based on CSB\nfeedback", ActivityType.TASK
                    )
                )
                node_Modify_screens_based.connect(node_Product, "")
                node_Bug.connect(node_Modify_screens_based, "")

        my_process_map.draw()
        my_process_map.save("images/test/test_sample07.png")


def test_sample08():
    with ProcessMap("Test Sample 08", colour_theme="TEALWATERS") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("start", EventType.START)
            t11 = lane1.add_element("Task 1-1", ActivityType.TASK)
            start.connect(t11)
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 2") as lane2:
                t21 = lane2.add_element("Task 2-1", ActivityType.TASK)
                g22 = lane2.add_element("Gateway 2-2", GatewayType.EXCLUSIVE)
                t23 = lane2.add_element("Task 2-3", ActivityType.TASK)
                t24 = lane2.add_element("Task 2-4", ActivityType.TASK)
                t11.connect(t21)
                t21.connect(g22)
                g22.connect(t21, "Yes")
                g22.connect(t23, "No")
            with pool1.add_lane("Lane 3") as lane3:
                g31 = lane3.add_element("Gateway 3-1", GatewayType.EXCLUSIVE)
                end = lane3.add_element("end", EventType.END)
                t23.connect(g31)
                g31.connect(t11, "Yes")
                g31.connect(t24, "No")
                t24.connect(end)

        my_process_map.draw()
        my_process_map.save("images/test/test_sample08.png")


def test_sample09():
    with ProcessMap("Test Sample 09", colour_theme="TEALWATERS") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("start", EventType.START)
            t11 = lane1.add_element("Task 1-1", ActivityType.TASK)
            start.connect(t11)
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 2") as lane2:
                t21 = lane2.add_element("Task 2-1", ActivityType.TASK)
                g22 = lane2.add_element("Gateway 2-2", GatewayType.EXCLUSIVE)
                t23 = lane2.add_element("Task 2-3", ActivityType.TASK)
                t24 = lane2.add_element("Task 2-4", ActivityType.TASK)
                t11.connect(t21)
                t21.connect(g22)
                g22.connect(t21, "Yes")
                g22.connect(t23, "No")
            with pool1.add_lane("Lane 3") as lane3:
                end = lane3.add_element("end", EventType.END)
                t23.connect(end)
                t24.connect(end)

        my_process_map.draw()
        my_process_map.save("images/test/test_sample09.png")


def test_sample10():
    with ProcessMap("Test Sample 10", colour_theme="RUBYRED") as my_process_map:
        with my_process_map.add_lane("Lane 1") as lane1:
            start = lane1.add_element("start", EventType.START)
            t11 = lane1.add_element("Task 1-1", ActivityType.TASK)
            start.connect(t11)
        with my_process_map.add_pool("Pool 1") as pool1:
            with pool1.add_lane("Lane 2") as lane2:
                t21 = lane2.add_element("Task 2-1", ActivityType.TASK)
                g22 = lane2.add_element("Gateway 2-2", GatewayType.EXCLUSIVE)
                t23 = lane2.add_element("Task 2-3", ActivityType.TASK)
                t24 = lane2.add_element("Task 2-4", ActivityType.TASK)
                t11.connect(t21)
                t21.connect(g22)
                g22.connect(t21, "Yes")
                g22.connect(t23, "No")
                t23.connect(t24)
            with pool1.add_lane("Lane 3") as lane3:
                g31 = lane3.add_element("Gateway 3-1", GatewayType.EXCLUSIVE)
                end = lane3.add_element("end", EventType.END)
                g31.connect(t11, "Yes")
                t24.connect(end)

        my_process_map.draw()
        my_process_map.save("images/test/test_sample10.png")


def test_sample11():
    with ProcessMap(
        "Are we living in simulation?", colour_theme="TEALWATERS"
    ) as process_map:
        with process_map.add_pool("The World") as pool:
            with pool.add_lane("You") as you:
                start = you.add_element("start", EventType.START)
                t1 = you.add_element("Form simulation hypotheses", ActivityType.TASK)
                t2 = you.add_element("Look for glitches", ActivityType.TASK)
                g1 = you.add_element(
                    "Did boss walk past twice \nin the same manner?",
                    GatewayType.EXCLUSIVE,
                )
                t3 = you.add_element("Ask a stranger life purpose", ActivityType.TASK)
                g2 = you.add_element(
                    "Responded 'huh?' \nlike NPC?", GatewayType.EXCLUSIVE
                )
                start.connect(t1)
                t1.connect(t2)
                t2.connect(g1)
                final_simulated = you.add_element(
                    "The World is simulated", ActivityType.TASK
                )
                final_not_simulated = you.add_element(
                    "The World is not simulated", ActivityType.TASK
                )
                g1.connect(final_simulated, "Yes")
                g1.connect(t3, "No")
                t3.connect(g2)
                g2.connect(final_not_simulated, "No")
                g2.connect(final_simulated, "Yes")
                end = you.add_element("end", EventType.END)
                final_not_simulated.connect(end)
                final_simulated.connect(end)

            # with pool.add_lane("Stranger") as stranger:
            #     st1 = stranger.add_element("Responded ", ActivityType.TASK)
            #     t3.connect(st1)
            #     st1.connect(g2)
        process_map.draw()
        process_map.save("images/test/test_sample11.png")





if __name__ == "__main__":
    # test_sample01()
    # test_sample02()
    # test_sample03()
    # test_sample04()
    # test_sample05()  # -- Test validation. Should fail
    # test_sample06()  # -- Test validation. Should fail
    # test_sample07()  # -- Test validation. Should fail
    # test_sample08()
    # test_sample09()  # -- Test validation. Should fail
    # test_sample10()  # -- Test validation. Should fail
    test_sample11()

