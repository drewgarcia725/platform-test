
type Case = {
  id: string;
  case_number: string;
  client: string;
  payer_name: string;
  denied_amount: number;
  status: string;
  priority: number;
};

const statusColors: Record<string, string> = {
  new: "bg-gray-200",
  in_review: "bg-yellow-200",
  approved: "bg-green-200",
  closed: "bg-blue-200",
};

export default function CaseTable({ cases }: { cases: Case[] }) {
  return (
    <table className="w-full border">
      <thead>
        <tr>
          <th>Case #</th>
          <th>Client</th>
          <th>Payer</th>
          <th>Amount</th>
          <th>Status</th>
          <th>Priority</th>
        </tr>
      </thead>
      <tbody>
        {cases.map((c) => (
          <tr key={c.id}>
            <td>{c.case_number}</td>
            <td>{c.client}</td>
            <td>{c.payer_name}</td>
            <td>${c.denied_amount}</td>
            <td>
              <span className={`px-2 py-1 rounded ${statusColors[c.status]}`}>
                {c.status}
              </span>
            </td>
            <td>{c.priority}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
