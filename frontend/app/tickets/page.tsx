import { Protected } from "@/components/auth/protected"; import { TicketsView } from "@/features/tickets/ticket-views"; export default function Tickets(){return <Protected><TicketsView/></Protected>}
