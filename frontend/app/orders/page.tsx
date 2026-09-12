import { Protected } from "@/components/auth/protected"; import { OrdersView } from "@/features/orders/order-views"; export default function Orders(){return <Protected><OrdersView/></Protected>}
