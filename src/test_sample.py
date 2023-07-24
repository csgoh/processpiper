from processpiper import ProcessMap, EventType, ActivityType, GatewayType


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
                t2 = lane1.add_element(
                    "T2", ActivityType.TASK
                )
                t3 = lane1.add_element(
                    "T3", ActivityType.TASK
                )
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
    from processpiper import ProcessMap, EventType, ActivityType, GatewayType
    with ProcessMap("Break Glass Process", colour_theme="BLUEMOUNTAIN") as my_process_map:
        with my_process_map.add_pool("Organisation") as pool1:
            with pool1.add_lane("ProductA User") as lane1:
                start = lane1.add_element("start", EventType.START)
                report_issue = lane1.add_element("Report connectivity issue", ActivityType.TASK)
            with pool1.add_lane("Service Desk") as lane2:
                triage = lane2.add_element("Triage", ActivityType.TASK)
                azure_ad_issue = lane2.add_element("Azure AD issue?", GatewayType.EXCLUSIVE)
                escalate_ist = lane2.add_element("Escalate to IST team", ActivityType.TASK)
                escalate_producta = lane2.add_element("Escalate to ProductA team", ActivityType.TASK)
                notify_user = lane2.add_element("Notify user", ActivityType.TASK)
                close_ticket = lane2.add_element("close", EventType.END)
            with pool1.add_lane("ProductA Administrator") as lane3:
                verify_issue = lane3.add_element("Verify Azure AD Authentication Issue", ActivityType.TASK)     
                contact_esd = lane3.add_element("Notify Vendor Service Desk", ActivityType.TASK)
                get_approval = lane3.add_element("Get break glass approval", ActivityType.TASK)
                document_approval = lane3.add_element("Document reason and approval", ActivityType.TASK)        
                access_account = lane3.add_element("Access to break glass account", ActivityType.TASK)
                notify_service_desk = lane3.add_element("Notify Service Desk", ActivityType.TASK)
                logout_account = lane3.add_element("logout from break glass account", ActivityType.TASK)        
                end = lane3.add_element("end", EventType.END)
        with my_process_map.add_pool("Vendor") as pool2:
            with pool2.add_lane("Service Desk") as lane4:
                fix_connectivity = lane4.add_element("Fix authentication issue", ActivityType.TASK)
                notify_admin = lane4.add_element("Notify ProductA Administrator", ActivityType.TASK)
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

if __name__ == "__main__":
    test_sample01()
    test_sample02()
    test_sample03()
